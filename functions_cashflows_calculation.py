
from prep_functions import *



#@title BASIC FUNCTIONS


class CashFlowSimulator:
    def __init__(self, purchase_year, horizon_year, house_value_t0, equity_contribution, mortgage_rate, loan_term, 
                 rent_amount, energy_bills_rent, rent_increase, airbnb_net_yield, 
                 tax_shield, tax_shield_interest, house_value_increase, 
                 manteinance_cost, energy_bills_purchase, service_cost, 
                 ground_lease, ground_lease_expiry, purchase_cost_net, 
                 property_tax_percentage, selling_cost_percentage, discount_rate,
                 rent_out_gross_income, rent_out_operating_expense, months_no_rent,
                 rent_out_income_tax_rate):

        self.purchase_year = purchase_year
        self.horizion_year = horizon_year
        self.house_value_t0 = house_value_t0
        self.equity_contribution = equity_contribution
        self.mortgage_rate = mortgage_rate
        self.loan_term = loan_term
        self.rent_amount = rent_amount
        self.energy_bills_rent = energy_bills_rent
        self.rent_increase = rent_increase
        self.airbnb_net_yield = airbnb_net_yield
        self.tax_shield = tax_shield
        self.tax_shield_interest = tax_shield_interest
        self.house_value_increase = house_value_increase
        self.manteinance_cost = manteinance_cost
        self.energy_bills_purchase = energy_bills_purchase
        self.service_cost = service_cost
        self.ground_lease = ground_lease
        self.ground_lease_expiry = ground_lease_expiry
        self.purchase_cost_net = purchase_cost_net
        self.property_tax_percentage = property_tax_percentage
        self.selling_cost_percentage = selling_cost_percentage
        self.discount_rate = discount_rate
        self.rent_out_gross_income = rent_out_gross_income
        self.months_no_rent = months_no_rent
        self.rent_out_income_tax_rate = rent_out_income_tax_rate
        self.rent_out_operating_expense = rent_out_operating_expense

    def calculate_house_value_over_years(self):
        house_value_year_values = [round(self.house_value_t0 * (1 + self.house_value_increase ) ** year) for year in range(1,46)]
        return house_value_year_values

    def calculate_mortgage_payments(self, purchase_year):
        house_value = self.house_value_t0*(1+self.house_value_increase)**purchase_year
        loan_value = house_value - self.equity_contribution    
        monthly_rate = self.mortgage_rate / 12
        n_payments = self.loan_term * 12
        mortgage_monthly_payment = loan_value * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
        
        mortgage_payments_year_values = [round(mortgage_monthly_payment*12*self.tax_shield) for year in range(1,46)]
        return mortgage_payments_year_values

    def calculate_annual_interest(self, purchase_year):
        house_value = self.house_value_t0*(1+self.house_value_increase)**purchase_year
        loan_value = house_value - self.equity_contribution    
        monthly_rate = self.mortgage_rate / 12
        n_payments = self.loan_term * 12
        mortgage_payments_list = self.calculate_mortgage_payments(purchase_year)
        
        annual_payment = round(pd.Series(mortgage_payments_list).mean()/self.tax_shield)
        


        annual_interest_payments = []
        
        # Calculate annual interest payments for each year
        for year in range(1,46):
            if year in range(purchase_year, purchase_year+self.loan_term+1):
                    
                # Calculate the interest for the year
                annual_interest = round(loan_value * self.mortgage_rate)

                # Apply the tax shield to the interest
                annual_interest_after_tax_shield = round(annual_interest * self.tax_shield)

                # Append the annual interest payment after tax shield to the list
                annual_interest_payments.append(annual_interest)

                # Calculate the principal payment for the year
                principal_payment = annual_payment - annual_interest

                # Update the remaining balance for the next year
                loan_value = max(0, loan_value - principal_payment)
            else:
                annual_interest_payments.append(0)
                
        return annual_interest_payments


    # Additional methods based on your initial script...
    def calculate_renting_out_income(self):
        if self.rent_out_operating_expense < 1:
            rent_out_net_operating_expense = round(self.rent_out_operating_expense*self.rent_out_gross_income)
        else:
            rent_out_net_operating_expense = self.rent_out_operating_expense

        
        rent_out_net_income = (self.rent_out_gross_income - rent_out_net_operating_expense)*(1-self.rent_out_income_tax_rate) - self.service_cost - self.ground_lease - self.manteinance_cost/12

        net_rent_income_year_values = [round(12*rent_out_net_income*(1+self.rent_increase)**year) for year in range(1,46)]

        return net_rent_income_year_values


    

    def calculate_loss_rent_empty_house(self):
        loss_rent_empty_house_year_values = []
        net_rent_income_year_values = self.calculate_renting_out_income()
        loss_rent_empty_house_year_values= [round(net_rent_income_year_values[year-1] * self.months_no_rent / 12) for year in range(1,46)]
        return loss_rent_empty_house_year_values

    def calculate_purchase_cost_future(self):
        purchase_cost_future_year_values = [round(self.purchase_cost_net*(1+self.house_value_increase/2)**year) for year in range(1,46)]
        return purchase_cost_future_year_values

    def calculate_property_tax(self):
        property_tax_year_values = [round(self.property_tax_percentage * self.house_value_t0*(1+self.house_value_increase)**year) for year in range(1,46)]
        return property_tax_year_values
    
    def calculate_energy_bills(self):
        energy_bills_year_values = [round((12 * self.energy_bills_purchase) * (1 + self.house_value_increase / 2) ** year) for year in range(1,46)]
        return energy_bills_year_values

    def calculate_service_cost(self):
        service_costs_year_values = [round((12 * self.service_cost) * (1 + self.house_value_increase / 2) ** year) for year in range(1,46)]
        return service_costs_year_values

    def calculate_manteinance_cost(self):
        manteinance_cost_year_values = [round(self.manteinance_cost * (1 + self.house_value_increase) ** year) for year in range(1,46)]
        return manteinance_cost_year_values

    def calculate_rent_expenses(self):
        rent_expenses_year_values = [round(12*self.rent_amount*(1+self.rent_increase)**year) for year in range(1,46)]
        return rent_expenses_year_values

    def calculate_rent_energy_bills(self):       
        energy_bills_rent_year_values = [round(12*self.energy_bills_rent*(1+self.house_value_increase/2)**year) for year in range (1,46)]
        return energy_bills_rent_year_values

    def calculate_airbnb_income(self):
        airbnb_income_year_values = [round((self.airbnb_net_yield * self.house_value_t0) * (1 + self.house_value_increase) ** year) for year in range(1,46)]
        return airbnb_income_year_values
    
    def calculate_ground_lease_expense(self):
        ground_lease_year_values = [round(0) for year in range(1,self.ground_lease_expiry+1)]  + [round(self.ground_lease*self.tax_shield_interest) for year in range(self.ground_lease_expiry+1, 46)]
        return ground_lease_year_values

    def calculate_discount_rate(self):
        discount_factor_year_values = [1 / (1 + self.discount_rate) ** year for year in range(1,46)]
        return discount_factor_year_values

    
    
    
    
    
    
    #OLD CODE THAT COULD BE POTENTIALLY REUSDE
    # def cash_flow_simulation(self, purchase_year):

    #     house_value = self.house_value_t0*(1+self.house_value_increase)**purchase_year
    #     house_terminal_value = round((self.house_value_t0*(1+self.house_value_increase)**45))
    #     year_values = [year for year in range(1,46)]
    
    #     purchase_cost_future = self.calculate_purchase_cost_future()
    #     property_tax = self.calculate_property_tax()

    #     df_cash_flows=pd.DataFrame()

    #     df_cash_flows['year'] = year_values
        
    #     df_cash_flows['discount_rate'] = self.calculate_discount_rate()
        
    #     df_cash_flows['house_value_over_years'] = self.calculate_house_value_over_years()
    #     df_cash_flows['mortgage_payments'] = self.calculate_mortgage_payments(purchase_year)
    #     df_cash_flows['interest_payments'] = self.calculate_annual_interest(purchase_year)
        
    #     df_cash_flows['energy_bills'] = self.calculate_energy_bills()
    #     df_cash_flows['service_costs'] = self.calculate_service_cost()
    #     df_cash_flows['manteinance_cost'] = self.calculate_manteinance_cost()
        
    #     df_cash_flows['renting_out_income'] = self.calculate_renting_out_income()
    #     df_cash_flows['loss_rent_empty_house'] = self.calculate_loss_rent_empty_house()  # Assuming 0 months_no_rent for simplicity
    #     df_cash_flows['airbnb_income'] = self.calculate_airbnb_income()
    #     df_cash_flows['ground_lease_expenses'] = self.calculate_ground_lease_expense()

    #     df_cash_flows['rent_expenses'] = self.calculate_rent_expenses()
    #     df_cash_flows['energy_bills_rent'] = self.calculate_rent_energy_bills()
        
    #     df_cash_flows['purchase_costs'] = np.where(df_cash_flows['year'] < 3,
    #                                                 purchase_cost_future,
    #                                                 np.array(purchase_cost_future) + np.array(property_tax))
        
    #     df_cash_flows['equity_accumulation'] = df_cash_flows['mortgage_payments'] - df_cash_flows['interest_payments']
    
    #     df_cash_flows['house_terminal_value'] = np.where(df_cash_flows['year'] < 45,
    #                                                         0,
    #                                                         house_terminal_value)
    
    #     df_cash_flows['total_renting_cashflow'] = df_cash_flows['rent_expenses'] + df_cash_flows['energy_bills_rent']
        
    #     df_cash_flows['house_purchasing_cashflow'] = df_cash_flows['mortgage_payments'] + df_cash_flows['energy_bills'] + df_cash_flows['ground_lease_expenses'] + df_cash_flows['manteinance_cost'] + df_cash_flows['service_costs'] - df_cash_flows['airbnb_income'] - df_cash_flows['house_terminal_value']
    
    #     df_cash_flows['mortgage_paid_cashflow'] = df_cash_flows['energy_bills'] + df_cash_flows['service_costs'] + df_cash_flows['manteinance_cost'] + df_cash_flows['ground_lease_expenses'] - df_cash_flows['airbnb_income'] - df_cash_flows['house_terminal_value']
    
  
    #     # Add any additional cash flow calculations as needed
    #     return df_cash_flows

    # def calculate_benefit_over_renting(self, df, purchase_year, is_discounted_cashflow = True):
        
    #     mortgage_paid_year = min(self.loan_term + purchase_year,45)

    #     if is_discounted_cashflow == True:
    #         df['discount_rate'] = df['discount_rate']
    #     else:
    #         df['discount_rate'] = 1
        
    #     df['discount_factor'] = np.where(is_discounted_cashflow)

    #     df['net_house_purchasing_cashflow'] = np.where(df['year']<purchase_year,
    #                                                     df['total_renting_cashflow']*df['discount_rate'],
    #                                                     np.where(df['year'] < mortgage_paid_year,
    #                                                     df['house_purchasing_cashflow']*df['discount_rate'],
    #                                                     df['mortgage_paid_cashflow']*df['discount_rate']))
        
    #     df['renting_cash_flow_discounted'] = round(df['discount_rate']*df['total_renting_cashflow'])

    #     df['purchasing_cost'] = np.where(df['year'] == purchase_year,
    #                                     df['purchase_costs']*df['discount_rate'],
    #                                     0)
        
    #     df['house_terminal_value'] = df['house_terminal_value']*df['discount_rate']

    #     df['overall_cashflow_house_purchase'] = round(df['net_house_purchasing_cashflow']+df['purchasing_cost'] - df['house_terminal_value'])

    #     df['benefit_over_rent'] = df['renting_cash_flow_discounted'] - df['overall_cashflow_house_purchase']

    #     return df['benefit_over_rent'].sum()




















