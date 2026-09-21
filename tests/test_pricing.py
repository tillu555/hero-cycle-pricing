from datetime import date

from app.services import PricingService


def test_price_history():

    service = PricingService()

    service.add_price(
        component_id=101,
        price=200,
        effective_from=date(2026, 1, 1)
    )

    service.add_price(
        component_id=101,
        price=230,
        effective_from=date(2026, 7, 1)
    )

    assert service.get_applicable_price(
        101,
        date(2026, 3, 1)
    ) == 200

    assert service.get_applicable_price(
        101,
        date(2026, 8, 1)
    ) == 230