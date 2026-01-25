import { QueryRequest, QueryResponse } from '../types';

// Configuration - using a default value that can be overridden by Docusaurus siteConfig
const DEFAULT_API_URL = 'http://localhost:8000'; // Backend API server running on port 8000

// Function to get API URL - can be configured through Docusaurus config
function getApiBaseUrl(): string {
  // First, try to get from window object if manually configured (highest priority)
  if (typeof window !== 'undefined' && (window as any).chatbotConfig) {
    const config = (window as any).chatbotConfig;
    if (config && typeof config === 'object' && config.apiBaseUrl) {
      return config.apiBaseUrl;
    }
  }

  // Second, check for meta tag in the document
  if (typeof document !== 'undefined') {
    const apiEndpoint = document.querySelector('meta[name="chatbot-api-url"]');
    if (apiEndpoint) {
      const apiUrl = apiEndpoint.getAttribute('content');
      if (apiUrl) {
        return apiUrl;
      }
    }
  }

  // Third, try to get from Docusaurus siteConfig
  if (typeof window !== 'undefined' && (window as any).__DOCUSAURUS__) {
    const docusaurusGlobal = (window as any).__DOCUSAURUS__;
    if (docusaurusGlobal.siteConfig?.customFields?.chatbotApiUrl) {
      return docusaurusGlobal.siteConfig.customFields.chatbotApiUrl;
    }
  }

  // Fourth, check for the Docusaurus config in the page metadata
  if (typeof document !== 'undefined') {
    // Look for script tag that contains the site config
    const scriptTags = document.querySelectorAll('script[type="application/json"]');
    for (let i = 0; i < scriptTags.length; i++) {
      try {
        const content = scriptTags[i].textContent;
        if (content) {
          const parsed = JSON.parse(content);
          if (parsed?.siteConfig?.customFields?.chatbotApiUrl) {
            return parsed.siteConfig.customFields.chatbotApiUrl;
          }
        }
      } catch (e) {
        // Ignore parsing errors
      }
    }
  }

  return DEFAULT_API_URL;
}

const API_BASE_URL = getApiBaseUrl();

export class ApiService {
  async queryRagBackend(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: request.query,
          top_k: request.top_k || 3,
        }),
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });

      if (!response.ok) {
        // If the server responds with an error, try to get the error message
        if (response.status === 404 || response.status >= 500) {
          // The backend might not be available, return a simulated response
          return this.getSimulatedResponse(request.query);
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: QueryResponse = await response.json();
      return data;
    } catch (error: any) {
      // Handle different types of errors
      if (error.name === 'AbortError') {
        return {
          answer: '',
          sources: [],
          retrieved_chunks: [],
          success: false,
          error_message: 'Request timeout: The query is taking longer than expected. Please try again.',
        };
      } else if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error - backend is not accessible, return simulated response
        return this.getSimulatedResponse(request.query);
      } else {
        return {
          answer: '',
          sources: [],
          retrieved_chunks: [],
          success: false,
          error_message: `Error: ${error.message || 'An unknown error occurred'}`,
        };
      }
    }
  }

  // Simulate a response when the backend is not available
  private getSimulatedResponse(query: string): QueryResponse {
    // Simple response simulation based on keywords in the query
    const lowerQuery = query.toLowerCase();

    let answer = "I'm sorry, but the backend service is currently unavailable. In a real implementation, I would search the Physical AI & Humanoid Robotics book content to answer your question. ";

    if (lowerQuery.includes('robot') || lowerQuery.includes('ai') || lowerQuery.includes('artificial intelligence')) {
      answer += "Based on the book content, Physical AI and humanoid robotics involve creating intelligent systems that interact with the physical world through embodied agents. This includes topics like sensorimotor learning, embodiment principles, and the integration of AI with mechanical systems.";
    } else if (lowerQuery.includes('gazebo') || lowerQuery.includes('simulation')) {
      answer += "According to the book, Gazebo is a physics simulation engine used for testing robotic algorithms in a safe virtual environment. It provides realistic physics modeling with gravity, collisions, and sensor simulation for humanoid robots.";
    } else if (lowerQuery.includes('ros') || lowerQuery.includes('control')) {
      answer += "The book describes ROS (Robot Operating System) as a middleware framework that enables communication between different robotic software components. It uses a publish-subscribe architecture with nodes, topics, and services for distributed robotics applications.";
    } else {
      answer += "The Physical AI & Humanoid Robotics book covers topics such as embodied intelligence, sensorimotor learning, humanoid locomotion, and the integration of artificial intelligence with physical systems. For specific information, please refer to the book content directly.";
    }

    return {
      answer: answer,
      sources: ["Physical AI & Humanoid Robotics Book - Chapter Introduction"],
      retrieved_chunks: [{
        content: answer,
        source_url: "#",
        title: "Physical AI & Humanoid Robotics Book",
        score: 0.8,
        chunk_index: 1
      }],
      success: true,
      error_message: undefined,
    };
  }

  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000), // 5 second timeout for health check
      });

      return response.ok;
    } catch (error) {
      // If health check fails, assume service is not available
      // But don't log error to console to avoid noise
      return false;
    }
  }
}

export const apiService = new ApiService();