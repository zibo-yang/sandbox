import Mathlib

namespace Sandbox

/-- The natural number `11` is prime. -/
lemma eleven_prime : Nat.Prime 11 := by
  norm_num

/-- The real number `√11` is irrational. -/
theorem irrational_sqrt_eleven : Irrational (Real.sqrt 11) := by
  have h := eleven_prime.irrational_sqrt
  rwa [Nat.cast_ofNat] at h

end Sandbox
