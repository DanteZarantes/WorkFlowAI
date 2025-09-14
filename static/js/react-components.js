// React Components for Interactive Features
const { useState, useEffect, useRef } = React;

// Interactive AI Chat Widget
function AIChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { type: 'bot', text: 'Hi! I\'m NeuralFlow AI. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;
        
        const userMessage = { type: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simulate AI response
        setTimeout(() => {
            const responses = [
                "I'd be happy to help you with AI solutions! What specific challenge are you facing?",
                "Our machine learning models can help with that. Would you like to schedule a consultation?",
                "That's a great question! Our team specializes in custom AI development. Let me connect you with an expert.",
                "Based on your needs, I recommend checking out our pricing plans. Would you like me to show you our solutions?"
            ];
            const botResponse = { type: 'bot', text: responses[Math.floor(Math.random() * responses.length)] };
            setMessages(prev => [...prev, botResponse]);
            setIsTyping(false);
        }, 1500);
    };

    return React.createElement('div', {
        className: 'chat-widget',
        style: {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            zIndex: 1000
        }
    }, [
        // Chat Button
        !isOpen && React.createElement('button', {
            key: 'chat-btn',
            onClick: () => setIsOpen(true),
            style: {
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #5b8cff, #764ba2)',
                border: 'none',
                color: 'white',
                fontSize: '1.5rem',
                cursor: 'pointer',
                boxShadow: '0 4px 20px rgba(91,140,255,.4)',
                animation: 'pulse 2s infinite'
            }
        }, React.createElement('i', { className: 'fas fa-robot' })),

        // Chat Window
        isOpen && React.createElement('div', {
            key: 'chat-window',
            style: {
                width: '350px',
                height: '500px',
                background: 'rgba(11,18,34,.95)',
                borderRadius: '16px',
                border: '1px solid rgba(91,140,255,.3)',
                backdropFilter: 'blur(20px)',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden'
            }
        }, [
            // Header
            React.createElement('div', {
                key: 'header',
                style: {
                    padding: '16px',
                    background: 'linear-gradient(135deg, #5b8cff, #764ba2)',
                    color: 'white',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }
            }, [
                React.createElement('div', { key: 'title' }, [
                    React.createElement('div', { key: 'name', style: { fontWeight: 'bold' } }, 'NeuralFlow AI'),
                    React.createElement('div', { key: 'status', style: { fontSize: '0.8rem', opacity: 0.9 } }, 'Online')
                ]),
                React.createElement('button', {
                    key: 'close',
                    onClick: () => setIsOpen(false),
                    style: {
                        background: 'none',
                        border: 'none',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '1.2rem'
                    }
                }, '×')
            ]),

            // Messages
            React.createElement('div', {
                key: 'messages',
                style: {
                    flex: 1,
                    padding: '16px',
                    overflowY: 'auto',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                }
            }, [
                ...messages.map((msg, i) => 
                    React.createElement('div', {
                        key: i,
                        style: {
                            alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start',
                            maxWidth: '80%',
                            padding: '12px',
                            borderRadius: '12px',
                            background: msg.type === 'user' 
                                ? 'linear-gradient(135deg, #5b8cff, #764ba2)'
                                : 'rgba(255,255,255,.1)',
                            color: '#e7ecf7',
                            fontSize: '0.9rem'
                        }
                    }, msg.text)
                ),
                isTyping && React.createElement('div', {
                    key: 'typing',
                    style: {
                        alignSelf: 'flex-start',
                        padding: '12px',
                        borderRadius: '12px',
                        background: 'rgba(255,255,255,.1)',
                        color: '#9fb0d9'
                    }
                }, 'AI is typing...')
            ]),

            // Input
            React.createElement('div', {
                key: 'input-area',
                style: {
                    padding: '16px',
                    borderTop: '1px solid rgba(91,140,255,.2)',
                    display: 'flex',
                    gap: '8px'
                }
            }, [
                React.createElement('input', {
                    key: 'input',
                    type: 'text',
                    value: input,
                    onChange: (e) => setInput(e.target.value),
                    onKeyPress: (e) => e.key === 'Enter' && sendMessage(),
                    placeholder: 'Type your message...',
                    style: {
                        flex: 1,
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid rgba(91,140,255,.3)',
                        background: 'rgba(255,255,255,.05)',
                        color: '#e7ecf7',
                        outline: 'none'
                    }
                }),
                React.createElement('button', {
                    key: 'send',
                    onClick: sendMessage,
                    style: {
                        padding: '12px 16px',
                        borderRadius: '8px',
                        border: 'none',
                        background: 'linear-gradient(135deg, #5b8cff, #764ba2)',
                        color: 'white',
                        cursor: 'pointer'
                    }
                }, React.createElement('i', { className: 'fas fa-paper-plane' }))
            ])
        ])
    ]);
}

// Interactive Pricing Calculator
function PricingCalculator() {
    const [apiCalls, setApiCalls] = useState(5000);
    const [models, setModels] = useState(3);
    const [support, setSupport] = useState('basic');
    
    const calculatePrice = () => {
        let basePrice = 29;
        if (apiCalls > 5000) basePrice = 99;
        if (apiCalls > 50000) basePrice = 299;
        
        const modelCost = Math.max(0, (models - 3) * 10);
        const supportCost = support === 'priority' ? 50 : support === 'dedicated' ? 200 : 0;
        
        return basePrice + modelCost + supportCost;
    };

    return React.createElement('div', {
        style: {
            background: 'rgba(255,255,255,.08)',
            border: '1px solid rgba(91,140,255,.3)',
            borderRadius: '16px',
            padding: '32px',
            backdropFilter: 'blur(20px)'
        }
    }, [
        React.createElement('h3', {
            key: 'title',
            style: { color: '#5b8cff', marginBottom: '24px', textAlign: 'center' }
        }, 'Calculate Your Custom Price'),
        
        React.createElement('div', {
            key: 'controls',
            style: { display: 'grid', gap: '20px', marginBottom: '24px' }
        }, [
            React.createElement('div', { key: 'api-calls' }, [
                React.createElement('label', {
                    style: { display: 'block', color: '#9fb0d9', marginBottom: '8px' }
                }, `API Calls per month: ${apiCalls.toLocaleString()}`),
                React.createElement('input', {
                    type: 'range',
                    min: 1000,
                    max: 100000,
                    step: 1000,
                    value: apiCalls,
                    onChange: (e) => setApiCalls(parseInt(e.target.value)),
                    style: { width: '100%', accentColor: '#5b8cff' }
                })
            ]),
            
            React.createElement('div', { key: 'models' }, [
                React.createElement('label', {
                    style: { display: 'block', color: '#9fb0d9', marginBottom: '8px' }
                }, `AI Models: ${models}`),
                React.createElement('input', {
                    type: 'range',
                    min: 1,
                    max: 25,
                    value: models,
                    onChange: (e) => setModels(parseInt(e.target.value)),
                    style: { width: '100%', accentColor: '#5b8cff' }
                })
            ]),
            
            React.createElement('div', { key: 'support' }, [
                React.createElement('label', {
                    style: { display: 'block', color: '#9fb0d9', marginBottom: '8px' }
                }, 'Support Level'),
                React.createElement('select', {
                    value: support,
                    onChange: (e) => setSupport(e.target.value),
                    style: {
                        width: '100%',
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid rgba(91,140,255,.3)',
                        background: 'rgba(255,255,255,.05)',
                        color: '#e7ecf7'
                    }
                }, [
                    React.createElement('option', { key: 'basic', value: 'basic' }, 'Basic Support'),
                    React.createElement('option', { key: 'priority', value: 'priority' }, 'Priority Support (+$50)'),
                    React.createElement('option', { key: 'dedicated', value: 'dedicated' }, 'Dedicated Support (+$200)')
                ])
            ])
        ]),
        
        React.createElement('div', {
            key: 'result',
            style: {
                textAlign: 'center',
                padding: '20px',
                background: 'linear-gradient(135deg, #5b8cff, #764ba2)',
                borderRadius: '12px',
                color: 'white'
            }
        }, [
            React.createElement('div', {
                key: 'price',
                style: { fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '8px' }
            }, `$${calculatePrice()}`),
            React.createElement('div', { key: 'period' }, 'per month')
        ])
    ]);
}

// Real-time Analytics Chart
function AnalyticsChart() {
    const [data, setData] = useState([]);
    const canvasRef = useRef(null);

    useEffect(() => {
        // Generate sample data
        const generateData = () => {
            const newData = [];
            for (let i = 0; i < 24; i++) {
                newData.push({
                    hour: i,
                    apiCalls: Math.floor(Math.random() * 1000) + 500,
                    accuracy: 85 + Math.random() * 10
                });
            }
            setData(newData);
        };

        generateData();
        const interval = setInterval(generateData, 5000); // Update every 5 seconds

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (!canvasRef.current || data.length === 0) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const { width, height } = canvas;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Draw grid
        ctx.strokeStyle = 'rgba(91,140,255,0.2)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 10; i++) {
            const y = (height / 10) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }

        // Draw API calls line
        ctx.strokeStyle = '#5b8cff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        data.forEach((point, i) => {
            const x = (width / (data.length - 1)) * i;
            const y = height - (point.apiCalls / 1500) * height;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // Draw points
        ctx.fillStyle = '#5b8cff';
        data.forEach((point, i) => {
            const x = (width / (data.length - 1)) * i;
            const y = height - (point.apiCalls / 1500) * height;
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    }, [data]);

    return React.createElement('div', {
        style: {
            background: 'rgba(255,255,255,.08)',
            border: '1px solid rgba(91,140,255,.3)',
            borderRadius: '16px',
            padding: '24px',
            backdropFilter: 'blur(20px)'
        }
    }, [
        React.createElement('h3', {
            key: 'title',
            style: { color: '#5b8cff', marginBottom: '20px' }
        }, 'Real-time API Usage'),
        React.createElement('canvas', {
            key: 'canvas',
            ref: canvasRef,
            width: 400,
            height: 200,
            style: { width: '100%', height: '200px' }
        }),
        React.createElement('div', {
            key: 'stats',
            style: {
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '16px',
                marginTop: '20px'
            }
        }, [
            React.createElement('div', {
                key: 'current',
                style: { textAlign: 'center' }
            }, [
                React.createElement('div', {
                    style: { fontSize: '1.5rem', fontWeight: 'bold', color: '#5b8cff' }
                }, data.length > 0 ? data[data.length - 1].apiCalls : 0),
                React.createElement('div', {
                    style: { color: '#9fb0d9', fontSize: '0.9rem' }
                }, 'Current Hour')
            ]),
            React.createElement('div', {
                key: 'avg',
                style: { textAlign: 'center' }
            }, [
                React.createElement('div', {
                    style: { fontSize: '1.5rem', fontWeight: 'bold', color: '#5b8cff' }
                }, data.length > 0 ? Math.round(data.reduce((sum, d) => sum + d.apiCalls, 0) / data.length) : 0),
                React.createElement('div', {
                    style: { color: '#9fb0d9', fontSize: '0.9rem' }
                }, '24h Average')
            ]),
            React.createElement('div', {
                key: 'accuracy',
                style: { textAlign: 'center' }
            }, [
                React.createElement('div', {
                    style: { fontSize: '1.5rem', fontWeight: 'bold', color: '#5b8cff' }
                }, data.length > 0 ? `${Math.round(data[data.length - 1].accuracy)}%` : '0%'),
                React.createElement('div', {
                    style: { color: '#9fb0d9', fontSize: '0.9rem' }
                }, 'Accuracy')
            ])
        ])
    ]);
}

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add chat widget to all pages
    const chatContainer = document.createElement('div');
    document.body.appendChild(chatContainer);
    ReactDOM.render(React.createElement(AIChatWidget), chatContainer);

    // Add pricing calculator to pricing page
    const pricingContainer = document.getElementById('pricing-calculator');
    if (pricingContainer) {
        ReactDOM.render(React.createElement(PricingCalculator), pricingContainer);
    }

    // Add analytics chart to analytics page
    const analyticsContainer = document.getElementById('analytics-chart');
    if (analyticsContainer) {
        ReactDOM.render(React.createElement(AnalyticsChart), analyticsContainer);
    }
});

// Add pulse animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);