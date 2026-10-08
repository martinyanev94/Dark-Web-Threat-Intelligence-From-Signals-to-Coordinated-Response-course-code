from casebook import CaseProfile, Ecosystem, build_mitigations, group_by_type

case = CaseProfile(
    case_id="case-trafficking-01",
    ecosystem=Ecosystem.HUMAN_TRAFFICKING,
    harms=("exploitation", "coercive control"),
)

mitigations = build_mitigations(case)
lanes = group_by_type(mitigations)
print(case.case_id)
print({key: [item.mitigation_id for item in values] for key, values in lanes.items()})
