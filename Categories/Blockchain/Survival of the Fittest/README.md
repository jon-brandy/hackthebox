# Survival of the Fittest
## DESCRIPTION:
Alex had always dreamed of becoming a warrior, but she wasn't particularly skilled. When the opportunity arose to join a group of seasoned warriors on a quest to a mysterious island filled with real-life monsters, she hesitated. But the thought of facing down fearsome beasts and emerging victorious was too tempting to resist, and she reluctantly agreed to join the group. As they made their way through the dense, overgrown forests of the island, Alex kept her senses sharp, always alert for the slightest sign of danger. But as she crept through the underbrush, sword drawn and ready, she was startled by a sudden movement ahead of her. She froze, heart pounding in her chest as she realized that she was face to face with her first monster.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given 2 solidity codes.

> Creature.sol

```sol
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Creature {
    
    uint256 public lifePoints;
    address public aggro;

    constructor() payable {
        lifePoints = 20;
    }

    function strongAttack(uint256 _damage) external{
        _dealDamage(_damage);
    }
    
    function punch() external {
        _dealDamage(1);
    }

    function loot() external {
        require(lifePoints == 0, "Creature is still alive!");
        payable(msg.sender).transfer(address(this).balance);
    }

    function _dealDamage(uint256 _damage) internal {
        aggro = msg.sender;
        lifePoints -= _damage;
    }
}
```

> Setup.sol

```sol
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Creature} from "./Creature.sol";

contract Setup {
    Creature public immutable TARGET;

    constructor() payable {
        require(msg.value == 1 ether);
        TARGET = new Creature{value: 10}();
    }
    
    function isSolved() public view returns (bool) {
        return address(TARGET).balance == 0;
    }
}
```

2. After opened the web applications, it seems we need to beat the enemy which has lifeStock of 20 (written in the Creature.sol) code.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ccb2fa8-22d0-4ded-a7f9-f50ead547f1e)


3. Anyway you can solve this challenge by reading the guideline page by clicking the `docs` option at the navbar.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4822cb8c-a106-4754-8362-594d9f3e2134)


4. So let's just go straight-forward.

### FLOW

```
We need to do cast send strongAttack() function or we can just do it again and again by cast call punch() function.
When the lifePoints of creature is 0, then we do cast send loot() to get the flag.
Then we can open the flag at the /flag endpoint.
```

```
/rpc is our endpoint for the attack --> either using strongAttack() or punch().
Then we can check the enemy lifepoint simply by cast call lifePoints()
Next after we killed the enemy, we cast send loot().
And just access /flag to grab our flag.
```

5. We just need to use the private key address (because we will use cast send) and the target address.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f0e0db27-d619-41a4-8053-af10e2966853)


> BEATING THE ENEMY

```
cast send --rpc-url http://ip:port/rpc --private-key private_key_address target_address "strongAttack(dataType)" value
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1bedeff5-53a3-4bd9-bc35-4614ae049221)



