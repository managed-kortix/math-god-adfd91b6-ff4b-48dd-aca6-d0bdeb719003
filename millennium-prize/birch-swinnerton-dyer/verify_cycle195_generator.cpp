#include <eclib/htconst.h>
#include <eclib/egr.h>
#include <eclib/marith.h>
#include <eclib/points.h>
#include <eclib/saturate.h>
#include <eclib/version.h>

#include <iostream>
#include <numeric>
#include <vector>

struct ComponentRecord {
    ZZ prime;
    std::vector<int> group;
    int exponent;
    std::vector<std::vector<int>> point_image;
};

static int group_exponent(const std::vector<int>& group)
{
    int exponent = 1;
    for (const int order : group)
        exponent = std::lcm(exponent, order);
    return exponent;
}

static void print_point_image(const std::vector<std::vector<int>>& image)
{
    std::cout << "[";
    for (std::size_t i = 0; i < image.size(); ++i) {
        if (i != 0)
            std::cout << ",";
        std::cout << image[i];
    }
    std::cout << "]";
}

int main()
{
    set_precision(200);
    initprimes("", 0);

    Curvedata curve(ZZ(1), ZZ(0), ZZ(1), ZZ(-46813),
                    ZZ(-3372156843), 1);
    const ZZ denominator = to_ZZ("395197");
    Point point(curve, to_ZZ("399030891253207") * denominator,
                to_ZZ("7009131418974188521075"),
                denominator * denominator * denominator);

    if (!point.isvalid()) {
        std::cerr << "FAIL: point is not on the curve\n";
        return 1;
    }

    std::vector<Point> points{point};
    const std::vector<Point> halves = point.division_points(2);
    const bigfloat point_height = height(point);
    const ZZ generated_subgroup_egr_index = egr_index(points, 1);
    const bigfloat egr_height_lower_bound_200 = lower_height_bound(curve, 1);

    set_precision(300);
    const bigfloat egr_height_lower_bound_300 = lower_height_bound(curve, 1);

    ComponentGroups component_groups(curve);
    CurveRed reduced_curve(curve);
    std::vector<ZZ> component_places = getbad_primes(reduced_curve);
    component_places.push_back(ZZ(0));
    std::vector<ComponentRecord> component_records;
    int global_component_exponent = 1;
    for (const ZZ& place : component_places) {
        const std::vector<int> group = component_groups.ComponentGroup(place);
        const int exponent = group_exponent(group);
        const std::vector<std::vector<int>> image =
            MapPointsToComponentGroup(component_groups, points, place);
        component_records.push_back({place, group, exponent, image});
        global_component_exponent = std::lcm(global_component_exponent, exponent);
    }

    saturator saturation(&curve, 1, 0);
    saturation.set_points(points);
    const ZZ index_bound = saturation.get_index_bound();

    if (generated_subgroup_egr_index != 1) {
        std::cerr << "FAIL: P is not in the everywhere-good-reduction subgroup\n";
        return 1;
    }
    for (const ComponentRecord& record : component_records) {
        for (const std::vector<int>& coordinates : record.point_image) {
            for (const int coordinate : coordinates) {
                if (coordinate != 0) {
                    std::cerr << "FAIL: P has a nonzero component-group coordinate\n";
                    return 1;
                }
            }
        }
    }
    if (global_component_exponent != 2) {
        std::cerr << "FAIL: global component-group exponent is not 2\n";
        return 1;
    }
    if (!halves.empty()) {
        std::cerr << "FAIL: P is divisible by 2 in E(Q)\n";
        return 1;
    }
    if (!(point_height < to_bigfloat(34))) {
        std::cerr << "FAIL: canonical-height upper comparison failed\n";
        return 1;
    }
    if (!(egr_height_lower_bound_200 > to_bigfloat(7)) ||
        !(egr_height_lower_bound_300 > to_bigfloat(7))) {
        std::cerr << "FAIL: eclib bigfloat EGR height comparison failed\n";
        return 1;
    }
    if (index_bound != 2) {
        std::cerr << "FAIL: saturation index bound is not 2\n";
        return 1;
    }

    std::vector<long> candidate_odd_primes;
    primevar prime;
    while (prime.value() <= index_bound) {
        if (prime.value() >= 3)
            candidate_odd_primes.push_back(prime.value());
        ++prime;
    }
    if (!candidate_odd_primes.empty()) {
        std::cerr << "FAIL: unexpected odd saturation prime\n";
        return 1;
    }

    std::cout << "ECLIB_VERSION=";
    show_version(std::cout);
    std::cout << "MODEL=[1,0,1,-46813,-3372156843]\n";
    std::cout << "POINT_PROJECTIVE=" << point << "\n";
    std::cout << "CANONICAL_HEIGHT=" << point_height << "\n";
    std::cout << "RATIONAL_HALVES_OF_P=" << halves << "\n";
    std::cout << "TWO_SATURATION=PROVED\n";
    for (const ComponentRecord& record : component_records) {
        std::cout << "COMPONENT_PLACE=";
        if (record.prime == 0)
            std::cout << "REAL";
        else
            std::cout << record.prime;
        std::cout << " GROUP=" << record.group
                  << " EXPONENT=" << record.exponent
                  << " P_IMAGE=";
        print_point_image(record.point_image);
        std::cout << "\n";
    }
    std::cout << "GLOBAL_COMPONENT_GROUP_EXPONENT="
              << global_component_exponent << "\n";
    std::cout << "INDEX_OF_EGR_SUBGROUP_IN_ZP="
              << generated_subgroup_egr_index << "\n";
    std::cout << "ECLIB_BIGFLOAT_EGR_HEIGHT_BOUND_PRECISION_200="
              << egr_height_lower_bound_200 << "\n";
    std::cout << "ECLIB_BIGFLOAT_EGR_HEIGHT_BOUND_PRECISION_300="
              << egr_height_lower_bound_300 << "\n";
    std::cout << "ECLIB_BIGFLOAT_BOUND_SCOPE=not_a_directed_interval; strict_comparison_replayed_at_200_and_300_digits\n";
    std::cout << "SATURATOR_GET_INDEX_BOUND_RESULT=" << index_bound << "\n";
    std::cout << "CANDIDATE_ODD_SATURATION_PRIMES="
              << candidate_odd_primes << "\n";
    std::cout << "ODD_SATURATION_CONCLUSION=subject_to_eclib_bigfloat_ANTS_bound\n";
    std::cout << "PASS_WITH_STATED_BIGFLOAT_SCOPE\n";
    return 0;
}
