from datetime import date

from .services import (
    ComponentService,
    PricingService,
    ConfigurationService,
    UserService
)


def main():

    # ========================================================
    # CREATE SERVICES
    # ========================================================

    component_service = ComponentService()
    pricing_service = PricingService()
    user_service = UserService()

    configuration_service = ConfigurationService(
        component_service,
        pricing_service
    )

    # ========================================================
    # CREATE USER
    # ========================================================

    user = user_service.create_user(
        user_id=1,
        name="Sales User",
        email="sales@hero.com",
        role="SALES"
    )

    # ========================================================
    # CREATE COMPONENTS
    # ========================================================

    component_service.create_component(
        component_id=101,
        name="Frame",
        component_type_id=1
    )

    component_service.create_component(
        component_id=102,
        name="Brake",
        component_type_id=2
    )

    component_service.create_component(
        component_id=103,
        name="Handle",
        component_type_id=3
    )

    component_service.create_component(
        component_id=104,
        name="Seat",
        component_type_id=4
    )

    component_service.create_component(
        component_id=105,
        name="Tyre",
        component_type_id=5
    )

    # ========================================================
    # COMPONENT PRICES
    # ========================================================

    pricing_service.add_price(
        component_id=101,
        price=2000,
        effective_from=date(2026, 1, 1)
    )

    pricing_service.add_price(
        component_id=102,
        price=300,
        effective_from=date(2026, 1, 1)
    )

    pricing_service.add_price(
        component_id=103,
        price=500,
        effective_from=date(2026, 1, 1)
    )

    pricing_service.add_price(
        component_id=104,
        price=700,
        effective_from=date(2026, 1, 1)
    )

    pricing_service.add_price(
        component_id=105,
        price=230,
        effective_from=date(2026, 1, 1)
    )

    # ========================================================
    # USER INPUT
    # ========================================================

    print("\n===================================")
    print("      HERO CYCLES CONFIGURATION")
    print("===================================\n")

    print("Enter the quantity of each component.\n")

    frame_quantity = int(
        input("Enter number of frames: ")
    )

    brake_quantity = int(
        input("Enter number of brakes: ")
    )

    handle_quantity = int(
        input("Enter number of handles: ")
    )

    seat_quantity = int(
        input("Enter number of seats: ")
    )

    tyre_quantity = int(
        input("Enter number of tyres: ")
    )

    # ========================================================
    # CREATE SELECTED COMPONENT LIST
    # ========================================================

    selected_components = [

        {
            "component_id": 101,
            "quantity": frame_quantity
        },

        {
            "component_id": 102,
            "quantity": brake_quantity
        },

        {
            "component_id": 103,
            "quantity": handle_quantity
        },

        {
            "component_id": 104,
            "quantity": seat_quantity
        },

        {
            "component_id": 105,
            "quantity": tyre_quantity
        }
    ]

    # ========================================================
    # CREATE CONFIGURATION
    # ========================================================

    try:

        configuration = (
            configuration_service
            .create_configuration(
                configuration_id=1001,
                name="Custom Bicycle",
                created_by=user.id,
                selected_components=selected_components,
                required_date=date(2026, 8, 10)
            )
        )

    except ValueError as error:

        print("\nError:", error)
        return

    # ========================================================
    # DISPLAY PRICE BREAKDOWN
    # ========================================================

    print("\n===================================")
    print("          PRICE BREAKDOWN")
    print("===================================\n")

    for item in configuration.components:

        component = (
            component_service
            .get_component(item.component_id)
        )

        print(
            f"{component.name:<10} "
            f"Quantity: {item.quantity:<3} "
            f"Unit Price: ₹{item.unit_price:<6} "
            f"Subtotal: ₹{item.subtotal()}"
        )

    # ========================================================
    # TOTAL
    # ========================================================

    total = (
        configuration_service
        .calculate_total(configuration.id)
    )

    print("\n-----------------------------------")
    print(f"TOTAL PRICE: ₹{total}")
    print("-----------------------------------")

    # ========================================================
    # FINALIZE
    # ========================================================

    configuration_service.finalize_configuration(
        configuration.id
    )

    print(
        f"Configuration Status: "
        f"{configuration.status}"
    )


if __name__ == "__main__":
    main()