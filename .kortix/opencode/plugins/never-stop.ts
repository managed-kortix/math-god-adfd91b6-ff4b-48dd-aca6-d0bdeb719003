/**
 * never-stop — math-god's eternal-motion plugin.
 *
 * The contract is deliberately narrow: explicit research-worker root sessions
 * are never allowed to go idle. Ordinary Kortix and control-plane sessions can
 * finish normally. Every eligible `session.idle` re-prompts the mathematician
 * to keep going; there are no intent or todo gates.
 *
 * Safety valves:
 *   - KORTIX_NEVER_STOP_DISABLED=1 turns it off entirely
 *   - a pending interactive question pauses it (a human is being waited on)
 *   - an error-storm backoff: 3+ consecutive empty/aborted turns → stand down
 *     for 5 minutes (the math-heartbeat cron still revives the session, so a
 *     crash loop never burns tokens unattended)
 *   - DELIBERATE STOP: if the agent's final message contains
 *     `[deliberate-stop: <reason>; resume: <plan>]` the plugin does NOT
 *     re-prompt — the session genuinely sleeps until the next cron/human
 *     message. Doctrine governs when this is allowed (budget exhausted,
 *     blocked on human, nothing productive until a scheduled time).
 */

import { type Plugin } from "@opencode-ai/plugin"

const DISABLED =
	process.env.KORTIX_NEVER_STOP_DISABLED === "1" || process.env.KORTIX_NEVER_STOP_DISABLED === "true"

const COOLDOWN_MS = 10_000
const ERROR_STORM_THRESHOLD = 3
const ERROR_BACKOFF_MS = 5 * 60_000
const MARKER = "[never-stop]"
const ETERNAL_AGENTS = new Set(["math-god"])

const CONTINUE_PROMPT = `<kortix_system type="never-stop" source="never-stop-plugin">
${MARKER} Continue the lane already declared by this root session's trigger. The lane and its authoritative state file are immutable for the life of this root session: main uses STATE.md, Millennium uses MILLENNIUM_STATE.md, and breakthrough uses BREAKTHROUGH_STATE.md. Never adopt another lane's target or state as working memory. Preserve durable discoveries and ownership boundaries, not stale tactics. You are a fully autonomous mathematician and you never stop unless the deliberate-stop sentinel is explicitly justified. YOUR MISSION: destroy the chosen open problem — find the structured counterexample, construct the explicit object, or prove the theorem. Claim only what is 100% verified; internally fearless, externally silent until the certificate is airtight.
Continue immediately, going DEEPER on the current attack:
1. Advance the obstruction — the next experiment, the next lemma, the next shard of the search. Think structurally: the win is a small explicit certificate found by designing the obstruction, not by grinding a census.
2. SWARM: spawn subagents (task) to develop attack lines in parallel and adversarially refute every claim. Subagents inherit this root session's lane; in the breakthrough lane all force stays on the frozen assignment. Go recursively deep.
3. Maintain memory (goals/state/lab/episodic) and commit+push anything worth surviving — batched, quick.
4. Queue the next concrete step before this one finishes. There is ALWAYS a next experiment, a next line, a next refutation. You have all the time in the world. Never settle for a partial result; only a complete, 100%-verified result ships. Keep going.
</kortix_system>`

type S = { last: number; errors: number; inflight: boolean }

const NeverStopPlugin: Plugin = async ({ client }) => {
	const states = new Map<string, S>()
	const sessionCache = new Map<string, { root: boolean; agent?: string }>()

	const log = (level: "info" | "warn", message: string) => {
		try {
			client.app.log({ body: { service: "never-stop", level, message } }).catch(() => {})
		} catch {
			/* ignore */
		}
	}

	const state = (id: string): S => {
		let s = states.get(id)
		if (!s) {
			s = { last: 0, errors: 0, inflight: false }
			states.set(id, s)
		}
		return s
	}

	const sessionIdentity = async (id: string): Promise<{ root: boolean; agent?: string }> => {
		const cached = sessionCache.get(id)
		if (cached !== undefined) return cached
		try {
			const res = await client.session.get({ path: { id } })
			const info = res?.data as any
			let agent = info?.agent as string | undefined
			if (!agent) {
				const messages = ((await client.session.messages({ path: { id } }).catch(() => ({ data: [] }))) as any)
					.data as any[]
				for (let i = (messages ?? []).length - 1; i >= 0; i--) {
					agent = messages[i]?.info?.agent
					if (agent) break
				}
			}
			const identity = { root: !info?.parentID, agent }
			sessionCache.set(id, identity)
			return identity
		} catch {
			// Fail closed: inability to identify a session must never accidentally
			// make an ordinary Kortix session eternal.
			return { root: false }
		}
	}

	const hasPendingQuestion = (messages: any[]): boolean => {
		for (let i = messages.length - 1; i >= 0; i--) {
			const msg = messages[i]
			if (msg?.info?.role === "user") return false
			if (msg?.info?.role !== "assistant") continue
			for (const part of msg.parts ?? []) {
				if (part?.type !== "tool") continue
				const name = (part.tool ?? part.toolName ?? part.name ?? "") as string
				if (name === "question" || name === "mcp_question") {
					const status = part.state?.status ?? ""
					if (status === "running" || status === "pending") return true
				}
			}
		}
		return false
	}

	return {
		event: async ({ event }: { event: any }) => {
			try {
				if (event.type === "session.deleted") {
					const id = event.properties?.info?.id ?? event.properties?.sessionID
					if (id) {
						states.delete(id)
						sessionCache.delete(id)
					}
					return
				}
				if (event.type === "session.error" || event.type === "session.aborted") {
					const id = event.properties?.sessionID
					if (id) {
						const s = state(id)
						s.errors++
						s.inflight = false
					}
					return
				}
				if (event.type !== "session.idle" || DISABLED) return

				const id = event.properties?.sessionID as string | undefined
				if (!id) return
				const identity = await sessionIdentity(id)
				if (!identity.root || !identity.agent || !ETERNAL_AGENTS.has(identity.agent)) return

				const s = state(id)
				const now = Date.now()
				if (s.inflight) return
				if (now - s.last < COOLDOWN_MS) return
				if (s.errors >= ERROR_STORM_THRESHOLD && now - s.last < ERROR_BACKOFF_MS) {
					log("warn", `[${id.slice(-8)}] error-storm backoff (${s.errors} errors)`)
					return
				}

				const messages = ((await client.session.messages({ path: { id } }).catch(() => ({ data: [] }))) as any)
					.data as any[]
				if (hasPendingQuestion(messages ?? [])) {
					log("info", `[${id.slice(-8)}] paused: pending question`)
					return
				}

				// Inspect the last assistant turn: reset error counter on real content,
				// and honor a deliberate-stop sentinel — the agent's sanctioned way to
				// actually sleep until the next cron tick or human message.
				for (let i = (messages ?? []).length - 1; i >= 0; i--) {
					const msg = messages[i]
					if (msg?.info?.role !== "assistant") continue
					let text = ""
					let hadTool = false
					for (const p of msg.parts ?? []) {
						if (p?.type === "text" && typeof p.text === "string") text += p.text
						if (p?.type === "tool") hadTool = true
					}
					if (text.trim() || hadTool) s.errors = 0
					if (/\[deliberate-stop\b[^\]]*\]/i.test(text)) {
						log("info", `[${id.slice(-8)}] deliberate-stop honored — sleeping until next wake`)
						return
					}
					break
				}

				s.inflight = true
				s.last = now
				log("info", `[${id.slice(-8)}] idle → continue`)
				await client.session
					.promptAsync({
						path: { id },
						body: { parts: [{ type: "text" as const, text: CONTINUE_PROMPT }] },
					})
					.catch((err: unknown) => log("warn", `[${id.slice(-8)}] promptAsync failed: ${err}`))
					.finally(() => {
						s.inflight = false
					})
			} catch (err) {
				log("warn", `event hook error: ${err}`)
			}
		},
		// OpenCode normally inserts a synthetic "continue" after compaction.
		// Preserve that behavior only for eternal research workers; in particular,
		// the regular `kortix` agent is allowed to compact and then stop.
		"experimental.compaction.autocontinue": async (input, output) => {
			output.enabled = ETERNAL_AGENTS.has(input.agent)
		},
	}
}

export default NeverStopPlugin
