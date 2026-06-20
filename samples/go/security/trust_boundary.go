package security

import (
	"fmt"
)

// TrustTier represents the trust level of a communication endpoint.
type TrustTier int

const (
	Untrusted TrustTier = 0
	Gateway   TrustTier = 1
	Trusted   TrustTier = 2
)

func (t TrustTier) String() string {
	switch t {
	case Untrusted:
		return "Untrusted"
	case Gateway:
		return "Gateway"
	case Trusted:
		return "Trusted"
	default:
		return "Unknown"
	}
}

// Validate ensures that a message only crosses one trust tier at a time.
func Validate(from, to TrustTier) error {
	diff := int(to) - int(from)
	if diff < 0 {
		diff = -diff
	}
	if diff > 1 {
		return fmt.Errorf("trust boundary violation: cannot jump from %s to %s (diff=%d)", from, to, diff)
	}
	return nil
}

// RunTrustBoundary demonstrates the Trust Boundary pattern.
func RunTrustBoundary() {
	fmt.Println("=== Trust Boundary Pattern ===")

	cases := []struct {
		from, to TrustTier
	}{
		{Untrusted, Gateway}, // allowed: +1
		{Gateway, Trusted},   // allowed: +1
		{Untrusted, Trusted}, // blocked: +2
		{Trusted, Untrusted}, // blocked: -2
	}

	for _, c := range cases {
		err := Validate(c.from, c.to)
		if err != nil {
			fmt.Printf("  %s -> %s: BLOCKED (%v)\n", c.from, c.to, err)
		} else {
			fmt.Printf("  %s -> %s: OK\n", c.from, c.to)
		}
	}

	fmt.Println()
}
