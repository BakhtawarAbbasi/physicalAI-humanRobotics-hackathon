---
title: Cognitive Planning with LLMs
sidebar_position: 2
---

# Cognitive Planning with LLMs

## Introduction

This chapter covers LLM-based cognitive planning techniques for translating natural language goals into ROS 2 action sequences. Large Language Models (LLMs) provide sophisticated cognitive planning capabilities that bridge the gap between human natural language and robotic action execution, enabling complex task decomposition and reasoning.

## Prerequisites

Before starting with LLM-based cognitive planning, ensure you have:
- Completed the Voice-to-Action chapter
- Working ROS 2 environment (Humble Hawksbill or later)
- LLM integration tools installed (OpenAI API, Hugging Face transformers, or similar)
- Understanding of ROS 2 action concepts and service calls
- Basic knowledge of natural language processing concepts

## LLM Integration Concepts

Large Language Models (LLMs) provide cognitive planning capabilities that transform high-level human instructions into executable robotic behaviors. These systems excel at understanding context, decomposing complex tasks, and generating structured outputs that can be mapped to robotic actions.

### Key Components

1. **Natural Language Understanding**: Interpreting user commands and goals with context awareness
2. **Task Decomposition**: Breaking complex goals into atomic, executable actions
3. **Knowledge Representation**: Storing and retrieving information about the world and robot capabilities
4. **Action Mapping**: Converting LLM outputs to structured ROS 2 action calls
5. **Feedback Integration**: Incorporating environmental feedback into planning decisions
6. **Error Recovery**: Handling failures and adapting plans dynamically

### LLM Architectures for Robotics

- **Generative Models**: GPT-style models for flexible text generation and reasoning
- **Encoder-Decoder Models**: T5-style models for structured input-output transformations
- **Specialized Models**: Domain-specific models fine-tuned for robotics tasks
- **Multimodal Models**: Models that can process both text and visual inputs

## Natural Language to ROS 2 Action Translation

Translating natural language goals into executable ROS 2 action sequences requires careful consideration of the mapping between human language and robotic capabilities.

### Translation Pipeline

1. **Intent Recognition**: Identifying the user's goal from natural language
2. **Entity Extraction**: Extracting relevant objects, locations, and parameters
3. **Task Decomposition**: Breaking complex goals into sequential actions
4. **Action Selection**: Choosing appropriate ROS 2 actions/services for each step
5. **Parameter Mapping**: Converting natural language parameters to ROS message fields
6. **Sequence Generation**: Ordering actions according to dependencies and constraints

### Mapping Strategies

1. **Template-based mapping**: Using predefined templates for common action patterns
2. **Semantic parsing**: Converting natural language to structured intermediate representations
3. **Chain-of-thought reasoning**: Breaking complex tasks into logical steps with reasoning
4. **Context-aware translation**: Incorporating environmental and robot state information
5. **Symbolic grounding**: Connecting language concepts to specific robot capabilities

### Example Translation Patterns

```python
# Natural Language: "Go to the kitchen and bring me a red cup"
# Translated to ROS 2 Actions:
# 1. Navigate to kitchen location
# 2. Detect and localize red cup
# 3. Plan grasp trajectory for cup
# 4. Execute grasp action
# 5. Navigate back to user
# 6. Execute place action (release cup)
```

## LLM Provider Configuration Examples

### OpenAI API Configuration

```python
import openai
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose

class LLMBasedPlanner:
    def __init__(self):
        # Initialize OpenAI API
        openai.api_key = rospy.get_param('~openai_api_key', '')
        self.client = openai.OpenAI(api_key=openai.api_key)

        # ROS publishers/subscribers for action execution
        self.nav_pub = rospy.Publisher('/move_base_simple/goal', Pose, queue_size=10)
        self.action_pub = rospy.Publisher('/robot_actions', String, queue_size=10)

    def generate_action_sequence(self, natural_language_goal):
        """
        Generate a sequence of ROS 2 actions from natural language goal
        """
        prompt = f"""
        You are a cognitive planner for a humanoid robot. Convert the following natural language goal
        into a sequence of specific robot actions in JSON format.

        Goal: "{natural_language_goal}"

        Return a JSON array of actions with the following structure:
        {{
          "action": "navigation|manipulation|perception|etc.",
          "target_location": "optional coordinates or location name",
          "object": "optional object name",
          "parameters": {{...}},
          "description": "human-readable description"
        }}

        Be specific about locations, objects, and parameters where possible.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for more consistent outputs
                response_format={"type": "json_object"}
            )

            action_sequence = response.choices[0].message.content
            return eval(action_sequence)  # In production, use json.loads safely
        except Exception as e:
            rospy.logerr(f"Error generating action sequence: {e}")
            return []
```

### Hugging Face Transformers Configuration

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class HuggingFacePlanner:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_plan(self, user_input):
        """
        Generate a plan using local Hugging Face model
        """
        input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token,
                                         return_tensors='pt')

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=input_ids.shape[1] + 100,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.7
            )

        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response[len(user_input):]  # Return only the generated part
```

## Practical Exercises for Cognitive Planning

### Exercise 1: Basic LLM-ROS Integration

1. Set up your LLM API credentials in the ROS parameter server
2. Create a simple node that accepts natural language goals as input
3. Implement the basic translation pipeline to convert goals to action sequences
4. Test with simple commands like "go to the table" or "pick up the ball"
5. Verify that the generated action sequences are valid and executable

### Exercise 2: Context-Aware Planning

1. Enhance your planner to incorporate environmental context
2. Integrate with perception systems to provide object and location information
3. Modify the LLM prompts to include current robot state and environment information
4. Test with commands that require contextual understanding (e.g., "the red cup near you")
5. Evaluate how context improves planning accuracy

### Exercise 3: Complex Task Decomposition

1. Implement chain-of-thought reasoning in your LLM prompts
2. Test with complex multi-step tasks (e.g., "bring me the blue pen from the desk")
3. Verify that the planner correctly decomposes tasks into atomic actions
4. Add error handling for failed actions and plan adaptation
5. Test robustness with various complex goals

## Planning Accuracy Considerations

### Factors Affecting Accuracy

1. **Prompt Engineering**: Well-crafted prompts significantly improve output quality
2. **Model Selection**: Different LLMs have varying strengths for planning tasks
3. **Context Length**: Longer contexts allow for more detailed planning but may confuse models
4. **Output Parsing**: Reliable parsing of LLM outputs is crucial for robotic action
5. **Domain Adaptation**: Models trained on robotics data may perform better than general models

### Strategies for Improvement

1. **Few-shot Learning**: Provide examples in the prompt to guide the model
2. **Chain-of-Thought Prompting**: Encourage step-by-step reasoning
3. **Structured Output Formats**: Require JSON or other structured formats
4. **Validation Layers**: Add validation to ensure generated actions are valid
5. **Iterative Refinement**: Allow the model to refine its plans based on feedback

### Error Handling and Recovery

- **Invalid Action Detection**: Check if generated actions are valid before execution
- **Plan Feasibility**: Verify that required objects/resources are available
- **Fallback Strategies**: Provide alternative plans when primary plan fails
- **Human-in-the-Loop**: Allow humans to correct or approve plans before execution

## Advanced Planning Techniques

### Hierarchical Task Networks (HTN)

```python
# Example HTN for "Serve Drink":
# SERVE_DRINK:
#   - FIND_DRINK
#     - DETECT_BOTTLE
#     - LOCALIZE_BOTTLE
#   - GRASP_BOTTLE
#     - PLAN_GRASP
#     - EXECUTE_GRASP
#   - NAVIGATE_TO_USER
#     - GET_USER_LOCATION
#     - PLAN_PATH
#     - FOLLOW_PATH
#   - PRESENT_DRINK
#     - ADJUST_GRIP
#     - MOVE_TO_PRESENT_POSE
```

### Symbolic Planning Integration

Combine LLM-based planning with classical symbolic planners like PDDL for more reliable execution of complex tasks.

## Summary

This chapter covered LLM-based cognitive planning for robotics applications. You learned about:
- LLM integration concepts and key components
- Natural language to ROS 2 action translation techniques
- LLM provider configuration examples (OpenAI, Hugging Face)
- Practical exercises for implementing cognitive planning
- Planning accuracy considerations and improvement strategies
- Advanced planning techniques like HTN and symbolic integration

The next chapter will cover the complete integration of VLA components into a cohesive autonomous humanoid system.

## Next Steps

Continue to the next chapter to learn about [Autonomous Humanoid Capstone Integration](./capstone).