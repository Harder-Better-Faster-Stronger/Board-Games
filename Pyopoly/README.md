**Rules of the Game**
**1. First you must create the characters for the game.**

  a. Each character should have a name, and a symbol, which is a
  single capital letter.
  
  b. There are at most two players for the game (a single player game
  can be used for testing).
  
**2. Starting funds should be 1500 Retriever Ducats. (It should be set in a
constant so that you can modify it for testing purposes).**

**3. Your game sequence should be the following:**

  a. Have the player roll two six sided dice (using random.randint).
  Remember that randint(1, 12) will produce a uniform distribution,
  but rolling two dice does not produce a uniform distribution, you
  should use randint(1, 6) twice and add the result.

  b. Move the player that number of spaces, equal to the roll results.

  c. If the property they land on has price -1, it is unpurchasable.

  d. If the property has price bigger than or equal to zero, it is
  purchasable.

    i. If the property is owned by someone else, pay them the
    rent required.

    ii. If the property is not owned, it can be purchased by the
    person who landed on the space.

  e. If the player owns the property they can pay the building cost to
  build a building on the land. If they do so, the rent charged to the
  other player when they land on it is the building-rent cost.

  f. A player cannot sell properties back to the bank, cannot
  mortgage the properties, and cannot trade them to the other
  player. (Unlike in real monopoly.)

  g. After the player has decided whether to buy a property on which
  they land or paid rent to its owner, they can choose to build the
  building for any land they own.

  h. The player then chooses to end their turn, and it becomes the
  other player's turn.

  i. If at any point, a player is required to pay more money than they
  have, they become insolvent, and lose the game. Since only two
  players are allowed, the game should end.

  j. Even if a player has properties with value greater than the debt,
  they still become insolvent.

  k. A player does not need to have all of the properties in a set to
  build the building for any particular property. As soon as the
  property is owned, the building can be constructed.

**4. If a player passes the start position (0) then they get the pass-go
amount of money, 200 by default, but this should be a constant so that
it can be modified for testing.

5. Spaces with price -1 cannot be bought but also have no effect, so you
pay nothing for landing on them and get nothing in return
**
