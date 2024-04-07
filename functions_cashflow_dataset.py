from functions_cashflows_calculation import *
import numpy as np


class processing_dataframe(CashFlowSimulator):

    def calculate_mortgage_payments_single_value(self, purchase_year):
        house_value = (
            self.house_value_t0 * (1 + self.house_value_increase) ** purchase_year
        )
        loan_value = house_value - self.equity_contribution
        monthly_rate = self.mortgage_rate / 12
        n_payments = self.loan_term * 12
        mortgage_monthly_payment = (
            loan_value
            * (monthly_rate * (1 + monthly_rate) ** n_payments)
            / ((1 + monthly_rate) ** n_payments - 1)
        )

        mortgage_yearly_payment = round(12 * mortgage_monthly_payment * self.tax_shield)
        return mortgage_yearly_payment

    def calculate_interest_payments(self, df):
        list_interest_payments = []
        list_purchase_years = list(
            df[df["year_last_purchase"] > 0]["year_last_purchase"].unique()
        )

        list_purchase_years.append(46)
        year_first_purchase = int(
            df[df["year_last_purchase"] != 0]["year_last_purchase"].min()
        )
        # Fill the interest payment with 0 for the years before the purchase of the house
        if year_first_purchase != 1:
            num_zeros = year_first_purchase - 1

            list_interest_payments = [0] * num_zeros  # Create a list of zeros

        for i in range(len(list_purchase_years) - 1):
            start_year = int(list_purchase_years[i])
            end_year = int(list_purchase_years[i + 1])
            interest_payments = self.calculate_annual_interest(start_year)
            list_interest_payments.extend(
                interest_payments[start_year - 1 : end_year - 1]
            )

        return list_interest_payments

    def calculate_static_values(self, df):

        df = df.copy()

        last_year_mortgage_payments = df["year_last_purchase"].max() + self.loan_term

        first_year_mortgage_payments = int(
            df[df["year_last_purchase"] != 0]["year_last_purchase"].min()
        )

        years_purchasing_house = list(df["year_last_purchase"].unique())

        years_begining_renting_out = list(df["year_last_rent_out"].unique())

        years_selling_house = list(df[df["action"] == "sell"]["year"].unique())

        df["discount_rate"] = self.calculate_discount_rate()

        purchase_cost_future = self.calculate_purchase_cost_future()
        property_tax = self.calculate_property_tax()

        df["house_value_over_years"] = self.calculate_house_value_over_years()

        df["energy_bills"] = self.calculate_energy_bills()
        df["service_costs"] = self.calculate_service_cost()
        df["manteinance_cost"] = self.calculate_manteinance_cost()

        df["renting_out_income"] = self.calculate_renting_out_income()
        df["loss_rent_empty_house"] = np.where(
            df["year"].isin(years_begining_renting_out),
            self.calculate_loss_rent_empty_house(),
            0,
        )

        # Assuming 0 months_no_rent for simplicity
        df["airbnb_income"] = self.calculate_airbnb_income()
        df["ground_lease_expenses"] = self.calculate_ground_lease_expense()

        df["rent_expenses"] = self.calculate_rent_expenses()
        df["energy_bills_rent"] = self.calculate_rent_energy_bills()

        df["purchase_costs"] = np.where(
            (df["year"] < 3) & (self.house_value_t0 < 510000),
            purchase_cost_future,
            np.array(purchase_cost_future) + np.array(property_tax),
        )

        df["purchase_costs"] = np.where(
            df["year"].isin(years_purchasing_house), df["purchase_costs"], 0
        )

        df["selling_costs"] = np.round(
            np.where(
                df["year"].isin(years_selling_house),
                self.selling_cost_percentage * df["house_value_over_years"],
                0,
            )
        )

        df["mortgage_payments"] = np.where(
            (df["year"] > last_year_mortgage_payments)
            | (df["year"] < first_year_mortgage_payments),
            0,
            df["year_last_purchase"].apply(
                lambda x: self.calculate_mortgage_payments_single_value(x)
            ),
        )

        df["interest_payments"] = self.calculate_interest_payments(df)

        df["equity_accumulation"] = np.where(
            df["year"] < first_year_mortgage_payments,
            0,
            round(df["mortgage_payments"] / self.tax_shield - df["interest_payments"]),
        )

        # Calculate Cashflows that will be used for income analysis
        df["loss_rent_empty_house"] = np.where(
            df["year"].isin(years_begining_renting_out), df["loss_rent_empty_house"], 0
        )

        df["cash_flow_renting_out"] = (
            df["renting_out_income"]
            - df["loss_rent_empty_house"]
            - df["mortgage_payments"]
        )

        df["renting_cashflow"] = df["rent_expenses"] + df["energy_bills_rent"]

        df["house_purchasing_cashflow"] = (
            df["mortgage_payments"]
            + df["energy_bills"]
            + df["ground_lease_expenses"]
            + df["manteinance_cost"]
            + df["service_costs"]
            - df["airbnb_income"]
            + df["purchase_costs"]
        )

        return df

    def calculate_processed_df(self, df):
        df = df.copy()
        df_processed = self.calculate_static_values(df)

        return df_processed
