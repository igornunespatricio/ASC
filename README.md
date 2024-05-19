# Arena Santa Clara - ASC ⚽

<img src="docs/assets/images/photoASC.jpeg" width=600>

Arena Santa Clara is a **footvolley group** with 2 courts in Copacabana, Rio de Janeiro, Brazil. 🏖️

The purpose of this repository is to hold the **code to compute the ASC footvolley ranking**.

The **points calculation** for each player at each match is based on the **quality of the opponents and the quality of the partner**. The quality of the players is measured by their balanced points until the prior day of the match. 

**On summary:**

- Each player starts with 100 points in the ranking
- Each player can reach a minimum of 10 points in the ranking (very unlikely to happen)
- There is no maximum limit of points a player can reach in the ranking
- At each match, a player can win/lose a maximum of 10 points (very unlikely to happen)

The **logic for the points** works by assigning **more points to players that partners with less skilled people**. The purpose is to be **more inclusive with less skilled players** who are less frequently included in a scenario where **they are not likely to be picked to play a match** (a very common scenario in Brazil's footvolley courts).

The logic for each match works as following: ⬇️

- If the player wins: 👍
    - The more skilled the opponents, the more points the player wins. The less skilled the opponents, the less points the player wins.
    - The less skilled the partner, the more points the player win. The more skilled your partner, the less points the player wins.
 
- If the player loses: 👎
  - The more skilled the oponents, the less points the player loses. The less skilled the opponents, the more points the player loses.
  - The less skilled the partner, the less points the player loses. The more skilled the partner, the more points the player loses.
 
 
More in deep explanation in the formula below.

$$
f_i(x) = \begin{cases} 
P^o_i \times (1-P^p_j), & \text{if player } i \text{ wins} \\
-(1-P^o_i) \times P^p_j, & \text{if player } i \text{ loses}
\end{cases}
$$

where $f_{i}(x)$ is the amount of points player $i$ win/lose in a match. $P^o_{i}$ measures the quality in points of opponents of player $i$ and $P^p_{j}$ measures the quality in points of partner of player $i$. $P^o_{i}$ and $P^p_{j}$ can be expressed as

$$
P^o_i = \frac{x_l + x_m}{\sum x_k}
$$

$$
P^p_j = \frac{x_j}{\sum x_k}
$$

where $x_k$ is the balanced points of player $k$ prior to the day the match occurs.
