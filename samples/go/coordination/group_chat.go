package coordination

import (
	"aip-samples/shared"
	"fmt"
)

// ChatMessage holds a single agent's contribution to a group chat.
type ChatMessage struct {
	Agent   string
	Content string
}

// GroupChat facilitates a multi-agent discussion round.
type GroupChat struct {
	members []*shared.FakeAgent
}

func newGroupChat(members []*shared.FakeAgent) *GroupChat {
	return &GroupChat{members: members}
}

// Round asks each member about the topic and returns the transcript.
func (gc *GroupChat) Round(topic string) []ChatMessage {
	var transcript []ChatMessage
	for _, agent := range gc.members {
		response := agent.Invoke("topic: " + topic)
		transcript = append(transcript, ChatMessage{Agent: agent.Name, Content: response})
	}
	return transcript
}

// RunGroupChat demonstrates the Group Chat pattern.
func RunGroupChat() {
	fmt.Println("=== Group Chat Pattern ===")

	members := []*shared.FakeAgent{
		shared.NewFakeAgent("Planner"),
		shared.NewFakeAgent("Designer"),
		shared.NewFakeAgent("Engineer"),
		shared.NewFakeAgent("QA"),
	}

	chat := newGroupChat(members)
	topic := "how to improve the onboarding flow"

	fmt.Printf("Group chat topic: %q\n", topic)
	fmt.Println("Transcript:")
	for _, msg := range chat.Round(topic) {
		fmt.Printf("  [%s] %s\n", msg.Agent, msg.Content)
	}
	fmt.Println()
}
