class MenuItem:
    def __init__(self, name: str, price: float = 0):
        self._name = name
        self._price = price
    
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, new_name: str):
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise TypeError("Invalid name. Must be a String")
    @property
    def price(self) -> float:
        return self._price
    @price.setter
    def price(self, new_price: float):
        if new_price >= 0:
            self._price = new_price
        else:
            raise ValueError("Invalid price. Must be greater or equal to 0")
        
    def calculate_total() ->float:
        raise NotImplementedError("Must be implemented by subclasses!")
    
class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, description: str, side_dish: str = None):
        super().__init__(name, price)
        self.__description = description
        self.side_dish = side_dish

    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, new_description: str):
        if isinstance(new_description, str):
            self.__description = new_description
        else:
            raise TypeError("Invalid description. Must be a String")

    def calculate_total(self) -> float:
        if self.side_dish:
            return round(self.price + 3,3)
        else:
            return self.price
    def __str__(self):
        return f"{self.name}, Side dish: {self.side_dish} --- ${self.calculate_total()}\n{self.description}"
    
class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size: int):
        super().__init__(name, price)
        self.__size = size

    @property
    def size(self) -> float:
        return self.__size
    @size.setter
    def size(self, new_size: float):
        if new_size >= 0:
            self.__size = new_size
        else:
            raise ValueError("Invalid Size. Must be greater or equal to 0")

    def calculate_total() -> float:
        raise NotImplementedError("Must be implemented by subclasses!")

class SoftDrink(Beverage):
    def __init__(self, name: str, price: float, size: int):
        super().__init__(name, price, size)
    def calculate_total(self) -> float:
        return self.price
    def __str__(self):
        return f"{self.name} --- ${self.calculate_total()}"

class HouseDrink(Beverage):
    def __init__(self, name: str, price: float, size: int, description: str):
        super().__init__(name, price, size)
        self.__description = description

    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, new_description: str):
        if isinstance(new_description, str):
            self.__description = new_description
        else:
            raise TypeError("Invalid description. Must be a String")
        
    def calculate_total(self) -> float:
        if self.size >= 1500:
            return self.price + 2
        else:
            return self.price
    def __str__(self):
        return f"{self.name} --- ${self.calculate_total()}\n{self.description}"

class Appetizer(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
    def calculate_total(self) -> float:
        return self.price
    def __str__(self):
        return f"{self.name} --- ${self.calculate_total()}"
    
class Dessert(MenuItem):
    def __init__(self, name: str, price: float, description: str):
        super().__init__(name, price)
        self.__description = description
    
    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, new_description: str):
        if isinstance(new_description, str):
            self.__description = new_description
        else:
            raise TypeError("Invalid description. Must be a String")
        
    def calculate_total(self) -> float:
        return self.price
    def __str__(self):
        return f"{self.name} --- ${self.calculate_total()}\n{self.description}"
        
class Order():
    def __init__(self):
        self.items: list = []
    def add_item(self, item: MenuItem):
        self.items.append(item)
    def calculate_total_bill(self) -> float:
        bill: float = 0
        main_course_bought: bool = any(isinstance(item, MainCourse) for item in self.items)
        dessert_amount: int = 0
        for item in self.items:
            if isinstance(item, Dessert):
                dessert_amount += 1
            if isinstance(item, Beverage) and main_course_bought:
                bill += (item.calculate_total() - 1.50)
            elif isinstance(item, Dessert) and dessert_amount >= 2:
                bill += (item.calculate_total() - 1.50)
            else:
                bill += item.calculate_total()
        return bill
    def __str__(self):
        result: str = "----Bill----\n"
        main_course_bought: bool = any(isinstance(item, MainCourse) for item in self.items)
        dessert_amount: int = 0
        for item in self.items:
            discount: float = 0
            if isinstance(item, Dessert):
                dessert_amount += 1
            if isinstance(item, Beverage) and main_course_bought:
                discount = 1.50
                result += f"{item.name} ${item.calculate_total() - discount}\n"
            elif isinstance(item, Dessert) and dessert_amount >= 2:
                discount = 1.50
                result += f"{item.name} ${item.calculate_total() - discount}\n"
            elif isinstance(item, MainCourse) and item.side_dish:
                result += f"{item.name} w/ {item.side_dish} ${item.calculate_total()}\n"
            else:
                result += f"{item.name} ${item.calculate_total()}\n"
        result += f"Total: ${round(self.calculate_total_bill(),3)}"
        return result
    
class PaymentMethod():
    def __init__():
        pass
    def pay(self):
        raise NotImplementedError("Must be implemented by subclasses!")
    
class CreditCard(PaymentMethod):
    def __init__(self, number: str, cvv: int):
        self.number = number
        self.cvv = cvv
    def pay(self, amount: float):
        print(f"Paying ${amount} with card {self.number[-4:]}")

class Cash(PaymentMethod):
    def __init__(self, remaining_amount: float):
        self.__remaining_amount = remaining_amount

    @property
    def remaining_amount(self):
        return self.__remaining_amount
    @remaining_amount.setter
    def remaining_amount(self, new_amount: float):
        if new_amount >= 0:
            self.__remaining_amount = new_amount
        else:
            raise ValueError("Invaid amount. Must be greater or equal to 0")
        
    def pay(self, amount: float):
        if self.remaining_amount < amount:
            print(f"Insufficient funds. ${amount - self.remaining_amount} missing to complete transaction")
        else:
            print(f"Payment in cash accepted. Change: {round(self.remaining_amount - amount, 3)}")
            new_amount = round(self.remaining_amount - amount, 3)
            self.remaining_amount = new_amount

if __name__ == "__main__":
        
    # Menu
    stk_fries = MainCourse("Steak",29.99,"300 gr of Ribeye, resting on a bed of mashed potatoes","Fries")
    stk_alone = MainCourse("Steak",29.99,"300 gr of Ribeye, resting on a bed of mashed potatoes")
    rib_salad = MainCourse("Pork Ribs",24.99,"250 gr of Ribs, accompanied with the 'House Sauce'","Salad")
    coke = SoftDrink("Coca-Cola",4.99,300)
    sprite = SoftDrink("Sprite",3.99,300)
    tea_pers = HouseDrink("Iced Tea",3.99,250,"Freshly prepared Iced Tea, with lemons")
    tea_jar = HouseDrink("Iced Tea",3.99,1500,"A Jar of our freshly prepared Iced Tea, with lemons")
    msc_mul = HouseDrink("Moscow Mule",8.99,300,"Iconic cocktail prepared in the House Bar")
    mozz_stix = Appetizer("Mozzarella Sticks", 8.49)
    onio_rinx = Appetizer("Crunchy Onion Rings", 7.49)
    tiramisu = Dessert("Tiramisu",6.99,"Sweet dessert for those who love coffe")
    red_velv = Dessert("Red Velvet Slice",6.99,"Velvety Vanilla cake for those with a sweet tooth")

    order_obj = Order()

    order_obj.add_item(stk_alone)
    order_obj.add_item(rib_salad)
    order_obj.add_item(mozz_stix)
    order_obj.add_item(tea_jar)
    order_obj.add_item(tiramisu)
    order_obj.add_item(red_velv)

    print(order_obj, "\n")

    card = CreditCard("1000123450098712", 321)
    card.pay(round(order_obj.calculate_total_bill(), 3))

    cash = Cash(100)
    cash.pay(round(order_obj.calculate_total_bill(), 3))
    print(f"Remaining cash: {cash.remaining_amount}")