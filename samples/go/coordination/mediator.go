package coordination

import (
	"fmt"
	"sync"
)

// MediatorMessage is a routable message passed through the mediator.
type MediatorMessage struct {
	From    string
	To      string
	Content string
}

// Mediator routes messages between agents via named channels.
type Mediator struct {
	mu       sync.Mutex
	channels map[string]chan MediatorMessage
}

func newMediator() *Mediator {
	return &Mediator{channels: make(map[string]chan MediatorMessage)}
}

func (m *Mediator) Register(name string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.channels[name] = make(chan MediatorMessage, 4)
}

func (m *Mediator) Send(msg MediatorMessage) {
	m.mu.Lock()
	ch, ok := m.channels[msg.To]
	m.mu.Unlock()
	if ok {
		ch <- msg
	}
}

func (m *Mediator) Receive(name string) MediatorMessage {
	m.mu.Lock()
	ch := m.channels[name]
	m.mu.Unlock()
	return <-ch
}

// RunMediator demonstrates the Mediator pattern.
func RunMediator() {
	fmt.Println("=== Mediator Pattern ===")

	med := newMediator()
	med.Register("Alice")
	med.Register("Bob")

	var wg sync.WaitGroup
	wg.Add(2)

	// Alice sends 2 messages to Bob and reads 2 from Bob
	go func() {
		defer wg.Done()
		med.Send(MediatorMessage{From: "Alice", To: "Bob", Content: "Hello Bob!"})
		med.Send(MediatorMessage{From: "Alice", To: "Bob", Content: "How are you?"})
		for i := 0; i < 2; i++ {
			msg := med.Receive("Alice")
			fmt.Printf("  Alice received from %s: %q\n", msg.From, msg.Content)
		}
	}()

	// Bob reads 2 from Alice then replies
	go func() {
		defer wg.Done()
		for i := 0; i < 2; i++ {
			msg := med.Receive("Bob")
			fmt.Printf("  Bob received from %s: %q\n", msg.From, msg.Content)
			med.Send(MediatorMessage{From: "Bob", To: "Alice", Content: "Got it: " + msg.Content})
		}
	}()

	wg.Wait()
	fmt.Println()
}
