const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface AgentResult {
  agent_id: number;
  name: string;
  category: string;
  price_per_call: number;
  overall_trust_score: number;
  reliability_score: number;
  latency_score: number;
  health_status: string;
  capabilities: string[];
}

export interface RecommendationResponse {
  results: AgentResult[];
  total_found: number;
}

export async function fetchRecommendations(capability: string, maxPrice?: number): Promise<RecommendationResponse | null> {
  try {
    let url = `${API_URL}/rankings/recommend?capability=${capability}`;
    if (maxPrice !== undefined) {
      url += `&max_price=${maxPrice}`;
    }
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });
    
    if (!response.ok) {
      console.error(`API Error: ${response.status}`);
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('Network Error:', error);
    return null;
  }
}
