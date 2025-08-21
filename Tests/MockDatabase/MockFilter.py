from unittest.mock import MagicMock

def make_filter_side_effect(mock_data):
    def filter_side_effect(*conditions):
        db = MagicMock()
        applied_conditions = []

        for cond in conditions:
            try:
                field = cond.left.name
                value = cond.right.value
                applied_conditions.append((field, value))
            except AttributeError:
                continue

        def all_side_effect():
            results = mock_data
            for field, value in applied_conditions:
                results = [
                    s for s in results
                    if str(getattr(s, field, None)) == str(value)
                ]
            return results

        def first_side_effect():
            results = all_side_effect()
            return results[0] if results else None

        # Assign side effects
        db.all.side_effect = all_side_effect
        db.first.side_effect = first_side_effect
        db.filter.side_effect = filter_side_effect

        return db

    return filter_side_effect
