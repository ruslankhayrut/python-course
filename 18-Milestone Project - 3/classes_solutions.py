"""
Flower Shop Ordering To Go
Create a flower shop application which deals in flower objects and use those 
flower objects in a bouquet object which can then be sold. Keep track of the number 
of objects and when you may need to order more.
"""


from random import choice

FLOWER_SPECIES = ['carnation', 'rose', 'arum-lily', 'sunflower', 'cornflower']


class Flower:
    def __init__(self, species: str) -> None:
        self.species = species

    def __str__(self) -> str:
        return self.species.capitalize()


class Bouquet:
    def __init__(self, flowers: list[Flower]) -> None:
        self.flowers: list[Flower] = flowers
        self.price = 8

    def __str__(self):
        flowers = {}

        for flower in self.flowers:
            flowers[str(flower)] = flowers[str(flower)] + \
                1 if str(flower) in flowers else 1

        return f'Bouqet contains:\n' + '\n'.join([f'{num} of {flower}' for flower, num in flowers.items()])


class FlowerShop:
    def __init__(self, flowers: list[Flower] = [], funds=200) -> None:
        self.flowers: list[Flower] = flowers
        self.funds = funds
        self.bouquets: list[Bouquet] = []
        self.sold_items: int = 0

    def order_flowers(self, quantity: int):
        if quantity > self.funds:
            raise ValueError(
                'Not enough funds for ordering that quantity of flowers')

        self.funds -= quantity

        for _ in range(quantity):
            self.flowers.append(Flower(choice(FLOWER_SPECIES)))

    def generate_bouquets(self):
        while len(self.flowers) >= 5:
            self.bouquets.append(Bouquet(self.flowers[:5]))
            self.flowers = self.flowers[5:]

    def sell_bouquet(self):
        if not self.bouquets:
            raise ValueError('No more bouqets, generate more to continue.')

        self.sold_items += 1
        bouquet = self.bouquets.pop(0)
        self.funds += bouquet.price


def print_statements():
    print(f'quntity of flowers in shop: {len(shop.flowers)}')
    print(f'quntity of bouquets in shop: {len(shop.bouquets)}')
    print(f'funds in shop: {shop.funds}')


shop = FlowerShop()
print('\nShop Started\n')
print_statements()

shop.order_flowers(54)
print('\nOrdering Flowers...\n')
print_statements()

shop.generate_bouquets()
print('\nGenerating bouquets...\n')
print_statements()

while shop.bouquets:
    shop.sell_bouquet()
print('\nSelling all bouquets...\n')
print_statements()

# Exceptions will ocure:
# shop.order_flowers(250)
# shop.sell_bouquet()
