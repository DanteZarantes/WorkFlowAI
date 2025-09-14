// Interactive API Testing Playground
class APIPlayground {
    constructor(container) {
        this.container = container;
        this.apiKey = 'demo-key-1234567890';
        this.baseUrl = 'https://api.neuralflow.ai/v1';
        this.init();
    }
    
    init() {
        this.container.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; height: 600px;">
                <div>
                    <h3 style="color: #5b8cff; margin-bottom: 20px;">API Request Builder</h3>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #9fb0d9; margin-bottom: 8px;">Endpoint</label>
                        <select id="api-endpoint" style="width: 100%; padding: 12px; background: rgba(255,255,255,.05); border: 1px solid rgba(91,140,255,.3); border-radius: 8px; color: #e7ecf7;">
                            <option value="/predict">POST /predict - Make Prediction</option>
                            <option value="/models">GET /models - List Models</option>
                            <option value="/analytics">GET /analytics - Get Analytics</option>
                            <option value="/models/train">POST /models/train - Train Model</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #9fb0d9; margin-bottom: 8px;">Request Body (JSON)</label>
                        <textarea id="request-body" rows="8" style="width: 100%; padding: 12px; background: #0d1117; border: 1px solid rgba(91,140,255,.3); border-radius: 8px; color: #e7ecf7; font-family: 'Courier New', monospace; resize: vertical;" placeholder='{\n  "model": "chatbot",\n  "input": "Hello, how can AI help my business?",\n  "temperature": 0.7\n}'></textarea>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #9fb0d9; margin-bottom: 8px;">Headers</label>
                        <div style="background: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid rgba(91,140,255,.3); font-family: 'Courier New', monospace; color: #9fb0d9; font-size: 0.9rem;">
                            Authorization: Bearer ${this.apiKey}<br>
                            Content-Type: application/json
                        </div>
                    </div>
                    
                    <button id="send-request" class="btn btn-primary btn-full">
                        <i class="fas fa-paper-plane"></i>
                        Send Request
                    </button>
                </div>
                
                <div>
                    <h3 style="color: #5b8cff; margin-bottom: 20px;">Response</h3>
                    
                    <div style="margin-bottom: 16px;">
                        <div style="display: flex; gap: 12px; align-items: center;">
                            <span style="color: #9fb0d9;">Status:</span>
                            <span id="response-status" style="padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">Ready</span>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 16px;">
                        <div style="display: flex; gap: 12px; align-items: center;">
                            <span style="color: #9fb0d9;">Response Time:</span>
                            <span id="response-time" style="color: #5b8cff; font-weight: 600;">-</span>
                        </div>
                    </div>
                    
                    <div>
                        <label style="display: block; color: #9fb0d9; margin-bottom: 8px;">Response Body</label>
                        <pre id="response-body" style="background: #0d1117; border: 1px solid rgba(91,140,255,.3); border-radius: 8px; padding: 16px; color: #e7ecf7; font-family: 'Courier New', monospace; white-space: pre-wrap; overflow-y: auto; height: 300px; margin: 0;">Click "Send Request" to see the response...</pre>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h4 style="color: #5b8cff; margin-bottom: 16px;">Code Examples</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <h5 style="color: #9fb0d9; margin-bottom: 12px;">Python</h5>
                        <pre style="background: #0d1117; border: 1px solid rgba(91,140,255,.3); border-radius: 8px; padding: 16px; color: #e7ecf7; font-family: 'Courier New', monospace; font-size: 0.85rem; overflow-x: auto; margin: 0;"><code>import requests

url = "${this.baseUrl}/predict"
headers = {
    "Authorization": "Bearer ${this.apiKey}",
    "Content-Type": "application/json"
}
data = {
    "model": "chatbot",
    "input": "Hello, how can AI help?"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())</code></pre>
                    </div>
                    
                    <div>
                        <h5 style="color: #9fb0d9; margin-bottom: 12px;">JavaScript</h5>
                        <pre style="background: #0d1117; border: 1px solid rgba(91,140,255,.3); border-radius: 8px; padding: 16px; color: #e7ecf7; font-family: 'Courier New', monospace; font-size: 0.85rem; overflow-x: auto; margin: 0;"><code>const response = await fetch('${this.baseUrl}/predict', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ${this.apiKey}',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        model: 'chatbot',
        input: 'Hello, how can AI help?'
    })
});

const data = await response.json();
console.log(data);</code></pre>
                    </div>
                    
                    <div>
                        <h5 style="color: #9fb0d9; margin-bottom: 12px;">cURL</h5>
                        <pre style="background: #0d1117; border: 1px solid rgba(91,140,255,.3); border-radius: 8px; padding: 16px; color: #e7ecf7; font-family: 'Courier New', monospace; font-size: 0.85rem; overflow-x: auto; margin: 0;"><code>curl -X POST "${this.baseUrl}/predict" \\
  -H "Authorization: Bearer ${this.apiKey}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "chatbot",
    "input": "Hello, how can AI help?"
  }'</code></pre>
                    </div>
                </div>
            </div>
        `;
        
        this.setupEventListeners();
        this.updateRequestBody();
    }
    
    setupEventListeners() {
        const endpointSelect = this.container.querySelector('#api-endpoint');
        const sendButton = this.container.querySelector('#send-request');
        
        endpointSelect.addEventListener('change', () => this.updateRequestBody());
        sendButton.addEventListener('click', () => this.sendRequest());
    }
    
    updateRequestBody() {
        const endpoint = this.container.querySelector('#api-endpoint').value;
        const requestBody = this.container.querySelector('#request-body');
        
        const examples = {
            '/predict': {
                model: 'chatbot',
                input: 'Hello, how can AI help my business?',
                temperature: 0.7
            },
            '/models': null,
            '/analytics': null,
            '/models/train': {
                model_name: 'custom-classifier',
                dataset_url: 'https://example.com/dataset.csv',
                parameters: {
                    epochs: 100,
                    batch_size: 32,
                    learning_rate: 0.001
                }
            }
        };
        
        const example = examples[endpoint];
        if (example) {
            requestBody.value = JSON.stringify(example, null, 2);
        } else {
            requestBody.value = '// No request body needed for GET requests';
        }
    }
    
    async sendRequest() {
        const endpoint = this.container.querySelector('#api-endpoint').value;
        const requestBody = this.container.querySelector('#request-body').value;
        const statusEl = this.container.querySelector('#response-status');
        const timeEl = this.container.querySelector('#response-time');
        const responseEl = this.container.querySelector('#response-body');
        
        // Show loading state
        statusEl.textContent = 'Loading...';
        statusEl.style.background = '#f59e0b';
        statusEl.style.color = 'white';
        
        const startTime = Date.now();
        
        try {
            // Simulate API call with realistic delay
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
            
            const endTime = Date.now();
            const responseTime = endTime - startTime;
            
            // Generate realistic mock response
            const mockResponse = this.generateMockResponse(endpoint, requestBody);
            
            // Update UI with success
            statusEl.textContent = '200 OK';
            statusEl.style.background = '#22c55e';
            statusEl.style.color = 'white';
            
            timeEl.textContent = `${responseTime}ms`;
            responseEl.textContent = JSON.stringify(mockResponse, null, 2);
            
        } catch (error) {
            // Handle error
            statusEl.textContent = '500 Error';
            statusEl.style.background = '#ef4444';
            statusEl.style.color = 'white';
            
            timeEl.textContent = 'Failed';
            responseEl.textContent = JSON.stringify({
                error: 'Internal Server Error',
                message: 'Something went wrong with the API request'
            }, null, 2);
        }
    }
    
    generateMockResponse(endpoint, requestBody) {
        const responses = {
            '/predict': {
                success: true,
                prediction: {
                    output: "AI can help your business by automating repetitive tasks, providing data-driven insights, improving customer service through chatbots, and optimizing operations for better efficiency and cost savings.",
                    confidence: 0.94,
                    model_version: "v2.1.0",
                    processing_time: "45ms"
                },
                usage: {
                    tokens_used: 127,
                    cost: 0.0023
                }
            },
            '/models': {
                models: [
                    {
                        id: "chatbot-v2",
                        name: "Advanced Chatbot",
                        status: "active",
                        accuracy: 94.2,
                        created_at: "2024-01-15T10:30:00Z"
                    },
                    {
                        id: "classifier-v1",
                        name: "Text Classifier",
                        status: "active", 
                        accuracy: 89.7,
                        created_at: "2024-01-10T14:20:00Z"
                    },
                    {
                        id: "predictor-v3",
                        name: "Sales Predictor",
                        status: "training",
                        accuracy: 87.3,
                        created_at: "2024-01-20T09:15:00Z"
                    }
                ],
                total: 3
            },
            '/analytics': {
                period: "last_30_days",
                metrics: {
                    total_requests: 45230,
                    successful_requests: 44891,
                    error_rate: 0.75,
                    avg_response_time: "67ms",
                    top_models: [
                        { name: "chatbot-v2", requests: 28450 },
                        { name: "classifier-v1", requests: 12380 },
                        { name: "predictor-v3", requests: 4400 }
                    ]
                },
                usage_by_day: Array.from({length: 30}, (_, i) => ({
                    date: new Date(Date.now() - (29-i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    requests: Math.floor(Math.random() * 2000) + 1000
                }))
            },
            '/models/train': {
                success: true,
                job_id: "train_" + Math.random().toString(36).substr(2, 9),
                status: "queued",
                estimated_time: "15-20 minutes",
                message: "Training job has been queued successfully"
            }
        };
        
        return responses[endpoint] || { error: "Endpoint not found" };
    }
}

// Initialize API Playground
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('api-playground');
    if (container) {
        new APIPlayground(container);
    }
});