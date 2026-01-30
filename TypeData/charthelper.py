from typechart import TYPECHART

TYPES = TYPECHART.keys()

class ChartHelper:
    
    @staticmethod
    def damageMultiplier(atkType: str, defType: str) -> float:
        """
        Returns the damage multiplier that is applied to 
        an attack of 'atkType' when used on a Pokemon of type
        'defType'.

        Args:
            atkType (str): The type of the attacking move.
            defType (str): The type of the defending Pokemon.

        Returns:
            float: The damage multiplier.
        """
        if atkType in TYPECHART[defType]["weakness"]: return 2.0
        if atkType in TYPECHART[defType]["resistance"]: return 0.5
        if atkType in TYPECHART[defType]["immunity"]: return 0.0
        return 1.0

class TypeCombo:
    """
    The type(s) of a pokemon.
    """
    
    type1: str
    """ A Pokemon's primary type. """
    type2: str | None
    """ A Pokemon's secondary type. Set to None for monotype Pokemon. """
    teraType: str | None
    """ A Pokemon's tera type. This is set to None iff the pokemon isn't terastalized. """
    
    def __init__(self, type1: str, type2: str | None = None, teraType: str | None = None):
        self.type1 = type1
        self.type2 = type2
        self.teraType = teraType
        
    def damageFromMove(self, atkType: str) -> float:
        """
        The damage a Pokemon with this type combo
        will take from a move of type 'atkType'.

        Args:
            atkType (str): The type of the attacking
            move this Pokemon is being hit by.
            
        Returns:
            float: The damage multiplier.
        """
        if self.teraType: return ChartHelper.damageMultiplier(atkType, self.teraType)
        multiplier: float = ChartHelper.damageMultiplier(atkType, self.type1)
        if self.type2: return multiplier * ChartHelper.damageMultiplier(atkType, self.type2)
        return multiplier
    
    def damageFromPokemon(self, atkPokemon: "TypeCombo") -> float:
        """
        The max damage multiplier a STAB move from the opponent's
        Pokemon can have on this Pokemon.

        Args:
            atkPokemon (TypeCombo): _description_

        Returns:
            float: _description_
        """
        maxMultiplier: float = 0.0
        if atkPokemon.type1 == atkPokemon.teraType:
            maxMultiplier = 2.0 * self.damageFromMove(atkPokemon.type1)
        else:
            maxMultiplier = 1.5 * self.damageFromMove(atkPokemon.type1)
        if atkPokemon.type2:
            if atkPokemon.type2 == atkPokemon.teraType:
                return max(maxMultiplier, 2.0 * self.damageFromMove(atkPokemon.type2))
            else:
                maxMultiplier = max(maxMultiplier, 1.5 * self.damageFromMove(atkPokemon.type2))
        if atkPokemon.teraType and atkPokemon.type1 != atkPokemon.teraType:
            return max(maxMultiplier, 1.5 * self.damageFromMove(atkPokemon.teraType))
        return maxMultiplier
    
    def matchup(self, opponent: "TypeCombo") -> int:
        """
        Determines if this Pokemon has a winning, losing,
        or neutral type matchup against the opponent Pokemon.

        Args:
            opponent (TypeCombo): The type of the opponent's Pokemon.

        Returns:
            int: 1 if this Pokemon has the type advantage against
            the opponent, -1 if the opponent has the type advantage,
            and 0 if it's a neutral matchup.
        """
        damageDealt = opponent.damageFromPokemon(self)
        damageTaken = self.damageFromPokemon(opponent)
        if damageDealt > damageTaken: return 1
        if damageDealt < damageTaken: return -1
        return 0
    
    