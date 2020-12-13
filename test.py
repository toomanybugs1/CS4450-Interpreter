# Pokemon master name
name = "Ash Ketchum"

# Pokemon Health Points
charmander_HP = 125
squirtle_HP = 110
bulbasaur_HP = 150

print("bulbasaur has " + str(bulbasaur_HP) + " HP")
difference = squirtle_HP - charmander_HP
print("squirtle has " + str(difference) + " more HP than charmander")

if charmander_HP < squirtle_HP or charmander_HP == squirtle_HP:
    charmander_HP += 4
    print("squirtle greater or same")

counter = 10

while counter > 0:
    print("Counter: " + str(counter))
    counter = counter - 1

charmander_HP += 20
print("and continue pls " + str(charmander_HP))
