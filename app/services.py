from datetime import date, timedelta

from .models import (
    User,
    Component,
    ComponentPrice,
    Configuration,
    ConfigurationComponent
)


# ============================================================
# COMPONENT SERVICE
# ============================================================

class ComponentService:

    def __init__(self):
        self.components = []

    def create_component(
        self,
        component_id: int,
        name: str,
        component_type_id: int
    ):
        component = Component(
            id=component_id,
            name=name,
            component_type_id=component_type_id
        )

        self.components.append(component)

        return component

    def get_component(self, component_id: int):

        for component in self.components:

            if component.id == component_id:
                return component

        raise ValueError("Component not found")

    def get_all_components(self):

        return self.components

    def deactivate_component(self, component_id: int):

        component = self.get_component(component_id)

        component.active = False

        return component


# ============================================================
# PRICING SERVICE
# ============================================================

class PricingService:

    def __init__(self):
        self.price_history = []

    # --------------------------------------------------------
    # ADD PRICE
    # --------------------------------------------------------

    def add_price(
        self,
        component_id: int,
        price: float,
        effective_from: date
    ):

        if price <= 0:
            raise ValueError(
                "Price must be greater than zero"
            )

        # Close the currently active price period
        # before creating the new price.
        for record in self.price_history:

            if (
                record.component_id == component_id
                and record.effective_to is None
                and record.effective_from < effective_from
            ):

                record.effective_to = (
                    effective_from - timedelta(days=1)
                )

        new_record = ComponentPrice(
            component_id=component_id,
            price=price,
            effective_from=effective_from
        )

        self.price_history.append(new_record)

        return new_record

    # --------------------------------------------------------
    # GET APPLICABLE PRICE
    # --------------------------------------------------------

    def get_applicable_price(
        self,
        component_id: int,
        required_date: date
    ):

        matching_prices = [
            record
            for record in self.price_history
            if (
                record.component_id == component_id
                and record.effective_from <= required_date
                and (
                    record.effective_to is None
                    or required_date <= record.effective_to
                )
            )
        ]

        if not matching_prices:

            raise ValueError(
                "No applicable price found"
            )

        # If multiple records match,
        # use the most recent effective price.
        latest_price = max(
            matching_prices,
            key=lambda record: record.effective_from
        )

        return latest_price.price

    # --------------------------------------------------------
    # GET PRICE HISTORY
    # --------------------------------------------------------

    def get_price_history(
        self,
        component_id: int
    ):

        return [
            record
            for record in self.price_history
            if record.component_id == component_id
        ]


# ============================================================
# CONFIGURATION SERVICE
# ============================================================

class ConfigurationService:

    def __init__(
        self,
        component_service: ComponentService,
        pricing_service: PricingService
    ):

        self.component_service = component_service
        self.pricing_service = pricing_service

        self.configurations = []

    # --------------------------------------------------------
    # CREATE CONFIGURATION
    # --------------------------------------------------------

    def create_configuration(
        self,
        configuration_id: int,
        name: str,
        created_by: int,
        selected_components: list,
        required_date: date
    ):

        items = []

        # Process every selected component
        for selected in selected_components:

            component_id = selected["component_id"]
            quantity = selected["quantity"]

            # ------------------------------------------------
            # Validate quantity
            # ------------------------------------------------

            if quantity <= 0:

                raise ValueError(
                    "Quantity must be greater than zero"
                )

            # ------------------------------------------------
            # Get component
            # ------------------------------------------------

            component = (
                self.component_service
                .get_component(component_id)
            )

            # ------------------------------------------------
            # Check component status
            # ------------------------------------------------

            if not component.active:

                raise ValueError(
                    f"{component.name} is inactive"
                )

            # ------------------------------------------------
            # Get applicable price
            # ------------------------------------------------

            unit_price = (
                self.pricing_service
                .get_applicable_price(
                    component_id,
                    required_date
                )
            )

            # ------------------------------------------------
            # Create configuration component
            # ------------------------------------------------

            item = ConfigurationComponent(
                component_id=component_id,
                quantity=quantity,
                unit_price=unit_price
            )

            items.append(item)

        # ----------------------------------------------------
        # Create complete configuration
        # ----------------------------------------------------

        configuration = Configuration(
            id=configuration_id,
            name=name,
            created_by=created_by,
            components=items
        )

        self.configurations.append(configuration)

        return configuration

    # --------------------------------------------------------
    # GET CONFIGURATION
    # --------------------------------------------------------

    def get_configuration(
        self,
        configuration_id: int
    ):

        for configuration in self.configurations:

            if configuration.id == configuration_id:
                return configuration

        raise ValueError(
            "Configuration not found"
        )

    # --------------------------------------------------------
    # CALCULATE TOTAL
    # --------------------------------------------------------

    def calculate_total(
        self,
        configuration_id: int
    ):

        configuration = (
            self.get_configuration(
                configuration_id
            )
        )

        return configuration.calculate_total()

    # --------------------------------------------------------
    # FINALIZE CONFIGURATION
    # --------------------------------------------------------

    def finalize_configuration(
        self,
        configuration_id: int
    ):

        configuration = (
            self.get_configuration(
                configuration_id
            )
        )

        configuration.status = "FINALIZED"

        return configuration


# ============================================================
# USER SERVICE
# ============================================================

class UserService:

    def __init__(self):

        self.users = []

    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    def create_user(
        self,
        user_id: int,
        name: str,
        email: str,
        role: str
    ):

        user = User(
            id=user_id,
            name=name,
            email=email,
            role=role
        )

        self.users.append(user)

        return user

    # --------------------------------------------------------
    # GET USER
    # --------------------------------------------------------

    def get_user(
        self,
        user_id: int
    ):

        for user in self.users:

            if user.id == user_id:
                return user

        raise ValueError(
            "User not found"
        )