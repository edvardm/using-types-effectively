{-# LANGUAGE GADTs #-}

data Spell a where
    Fireball :: Int -> Spell Int
    Heal     :: Int -> Spell Bool
    Revive   :: Spell Bool

castSpell :: Spell a -> a
castSpell (Fireball dmg) = dmg  -- Returns damage dealt (Int)
castSpell (Heal amount)  = amount > 0  -- Returns success (Bool)
castSpell Revive         = True  -- Always succeeds (Bool)

-- Example usage
dmg :: Int
dmg = castSpell (Fireball 10)  --  10

success :: Bool
success = castSpell (Heal 15)  --  True

resurrected :: Bool
resurrected = castSpell Revive  --  True
