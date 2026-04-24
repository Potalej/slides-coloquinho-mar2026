MODULE funcoes
  IMPLICIT NONE
  PUBLIC energia_total
CONTAINS

SUBROUTINE energia_total (massas, qs, ps, G, eps, E)
  REAL(16), INTENT(IN)  :: massas(:), qs(:,:), ps(:,:)
  REAL(8), INTENT(IN)   :: G, eps
  REAL(16), INTENT(OUT) :: E
  REAL(16) :: T, V, rab(3), dist
  INTEGER  :: a, b

  T = 0.0
  V = 0.0
  DO a = 1, SIZE(massas)
    T = T + DOT_PRODUCT(ps(a,:), ps(a,:)) / (2.0 * massas(a))
    DO b = 1, a - 1
      rab = qs(b,:) - qs(a,:)
      dist = DOT_PRODUCT(rab, rab) + eps*eps
      dist = SQRT(dist)

      V = V - G * massas(a) * massas(b) / dist
    END DO
  END DO

  E = T + V

END SUBROUTINE

END MODULE funcoes