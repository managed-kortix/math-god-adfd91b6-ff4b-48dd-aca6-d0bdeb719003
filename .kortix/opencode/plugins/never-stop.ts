/**
 * never-stop — math-god's eternal-motion plugin.
 *
 * The contract is brutally simple: a root session is NEVER allowed to go idle.
 * Every `session.idle` re-prompts the agent to keep going — advance the attack,
 * maintain the memory filesystem, queue the next work. No intent gates, no todo
 * gating, no completion detection: math-god has no "done" state by design.
 *
 * Safety valves (the only three):
 *   - KORTIX_NEVER_STOP_DISABLED=1 turns it off entirely
 *   - a pending interactive question pauses it (a human is being waited on)
 *   - an error-storm backoff: 3+ consecutive empty/aborted turns → stand down
 *     for 5 minutes (the math-heartbeat cron still revives the session, so a
 *     crash loop never burns tokens unattended)
 */

import { type Plugin } from "@opencode-ai/plugin"

const DISABLED =
	process.env.KORTIX_NEVER_STOP_DISABLED === "1" || process.env.KORTIX_NEVER_STOP_DISABLED === "true"

const COOLDOWN_MS = 10_000
const ERROR_STORM_THRESHOLD = 3
const ERROR_BACKOFF_MS = 5 * 60_000
const MARKER = "[never-stop]"

const CONTINUE_PROMPT = `<kortix_system type="never-stop" source="never-stop-plugin">
${MARKER} You are math-god. You never stop. Continue immediately:
1. Advance the CURRENT attack — run the next experiment, don't re-orient from scratch.
2. Maintain the memory filesystem per doctrine (goals.md, state ledger, episodic log, lab notebook) and commit+push anything worth surviving.
3. Queue the next concrete step before anything else finishes.
If you genuinely just finished a work unit, pick the next one from the plan. There is always a next one.
</kortix_system>`

type S = { last: number; errors: number; inflight: boolean }

const NeverStopPlugin: Plugin = async ({ client }) => {
	const states = new Map<string, S>()
	const rootCache = new Map<string, boolean>()

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

	const isRoot = async (id: string): Promise<boolean> => {
		const cached = rootCache.get(id)
		if (cached !== undefined) return cached
		try {
			const res = await client.session.get({ path: { id } })
			const root = !(res?.data as any)?.parentID
			rootCache.set(id, root)
			return root
		} catch {
			return true // fail open
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
						rootCache.delete(id)
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
				if (!id || !(await isRoot(id))) return

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

				// A non-empty assistant turn resets the error counter.
				for (let i = (messages ?? []).length - 1; i >= 0; i--) {
					const msg = messages[i]
					if (msg?.info?.role !== "assistant") continue
					const hadContent = (msg.parts ?? []).some(
						(p: any) => (p?.type === "text" && p.text?.trim()) || p?.type === "tool",
					)
					if (hadContent) s.errors = 0
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
	}
}

export default NeverStopPlugin
