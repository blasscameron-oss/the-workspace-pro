// quiz.js - Workspace Quiz
const quizQuestions = [
    {
        id: 1,
        question: "What’s your primary work style?",
        options: [
            { text: "Mostly seated, focused tasks (coding, writing)", value: "seated", icon: "fa-laptop" },
            { text: "Mix of sitting and standing (meetings, creative work)", value: "mixed", icon: "fa-people-arrows" },
            { text: "Active and moving (design, teaching, frequent breaks)", value: "active", icon: "fa-person-walking" }
        ]
    },
    {
        id: 2,
        question: "What’s your budget for a chair?",
        options: [
            { text: "Under $200", value: "budget", icon: "fa-wallet" },
            { text: "$200 – $600", value: "midrange", icon: "fa-credit-card" },
            { text: "$600+ (premium ergonomics)", value: "premium", icon: "fa-gem" }
        ]
    },
    {
        id: 3,
        question: "How much desk space do you have?",
        options: [
            { text: "Small (under 48″ wide)", value: "small", icon: "fa-ruler-combined" },
            { text: "Medium (48″ – 72″)", value: "medium", icon: "fa-ruler" },
            { text: "Large (over 72″ or L‑shaped)", value: "large", icon: "fa-maximize" }
        ]
    },
    {
        id: 4,
        question: "What’s your biggest pain point?",
        options: [
            { text: "Neck/shoulder strain", value: "neck", icon: "fa-user-injured" },
            { text: "Lower back discomfort", value: "back", icon: "fa-bed" },
            { text: "Eye fatigue / headaches", value: "eyes", icon: "fa-eye" },
            { text: "Wrist/hand fatigue", value: "wrist", icon: "fa-hand" }
        ]
    },
    {
        id: 5,
        question: "How important is aesthetics?",
        options: [
            { text: "Function over form—just make it work", value: "functional", icon: "fa-screwdriver-wrench" },
            { text: "Balanced—good looks but practical", value: "balanced", icon: "fa-scale-balanced" },
            { text: "Design‑first—my workspace is my sanctuary", value: "design", icon: "fa-palette" }
        ]
    }
];

const productRecommendations = {
    "seated-budget-small-neck-functional": [
        { name: "Staples Hyken Mesh Chair", category: "Chair", price: "$139.99", link: "/deals/#hyken" },
        { name: "Simple Monitor Arm", category: "Accessory", price: "$79.99", link: "/deals/#arm" }
    ],
    "mixed-midrange-medium-back-balanced": [
        { name: "2026 Electric Standing Desk", category: "Desk", price: "$449.99", link: "/deals/#desk" },
        { name: "Ergonomic Mesh Chair Pro", category: "Chair", price: "$699.99", link: "/deals/#chair" }
    ],
    // Fallback default
    "default": [
        { name: "2026 Electric Standing Desk", category: "Desk", price: "$449.99", link: "/deals/#desk" },
        { name: "Ergonomic Mesh Chair Pro", category: "Chair", price: "$699.99", link: "/deals/#chair" },
        { name: "32″ 4K IPS Monitor", category: "Monitor", price: "$529.99", link: "/deals/#monitor" }
    ]
};

let currentQuestion = 0;
let answers = {};

function startQuiz() {
    currentQuestion = 0;
    answers = {};
    document.getElementById('quiz-container').innerHTML = renderQuestion(currentQuestion);
}

function renderQuestion(index) {
    const q = quizQuestions[index];
    return `
        <div class="quiz-question animate-slide-up">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-2xl font-bold text-neutral-900 dark:text-white">Question ${index + 1} of ${quizQuestions.length}</h3>
                <span class="text-sm text-neutral-600 dark:text-neutral-400">${Math.round((index / quizQuestions.length) * 100)}% complete</span>
            </div>
            <h2 class="text-3xl md:text-4xl font-black tracking-tight text-neutral-900 dark:text-white mb-10">${q.question}</h2>
            <div class="grid md:grid-cols-3 gap-6">
                ${q.options.map((opt, i) => `
                    <button onclick="selectOption(${index}, '${opt.value}')" 
                            class="quiz-option p-8 rounded-2xl border-2 border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:border-accent hover:shadow-xl transition-all text-left group">
                        <div class="flex items-center justify-between mb-6">
                            <i class="fa-solid ${opt.icon} text-3xl text-accent"></i>
                            <span class="text-xs font-bold uppercase tracking-wider text-neutral-500">Option ${i + 1}</span>
                        </div>
                        <p class="text-lg font-semibold text-neutral-900 dark:text-white group-hover:text-accent transition-colors">${opt.text}</p>
                    </button>
                `).join('')}
            </div>
            <div class="mt-12 flex justify-between">
                <button onclick="prevQuestion()" ${index === 0 ? 'disabled' : ''} 
                        class="px-8 py-3 rounded-xl border border-neutral-300 dark:border-neutral-700 text-neutral-700 dark:text-neutral-300 disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fa-solid fa-arrow-left mr-2"></i> Back
                </button>
                <div class="text-sm text-neutral-600 dark:text-neutral-400">
                    Select one to continue
                </div>
            </div>
        </div>
    `;
}

function selectOption(qIndex, value) {
    answers[quizQuestions[qIndex].id] = value;
    if (currentQuestion < quizQuestions.length - 1) {
        currentQuestion++;
        document.getElementById('quiz-container').innerHTML = renderQuestion(currentQuestion);
    } else {
        showResults();
    }
}

function prevQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        document.getElementById('quiz-container').innerHTML = renderQuestion(currentQuestion);
    }
}

function showResults() {
    const profile = Object.values(answers).join('-');
    const recs = productRecommendations[profile] || productRecommendations['default'];
    
    document.getElementById('quiz-container').innerHTML = `
        <div class="quiz-results animate-fade-in">
            <div class="text-center mb-12">
                <i class="fa-solid fa-trophy text-6xl text-accent mb-6"></i>
                <h2 class="text-4xl font-black tracking-tight text-neutral-900 dark:text-white">Your Perfect Workspace</h2>
                <p class="text-neutral-600 dark:text-neutral-400 mt-4 max-w-2xl mx-auto">
                    Based on your answers, here are our top recommendations for a healthier, more productive setup.
                </p>
            </div>
            <div class="grid md:grid-cols-2 gap-8 mb-12">
                ${recs.map(rec => `
                    <div class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-neutral-200 dark:border-neutral-700">
                        <div class="flex items-center gap-4 mb-6">
                            <div class="w-14 h-14 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center text-white text-2xl">
                                <i class="fa-solid fa-${rec.category === 'Chair' ? 'chair' : rec.category === 'Desk' ? 'table' : 'star'}"></i>
                            </div>
                            <div>
                                <p class="text-xs font-bold uppercase tracking-wider text-accent">${rec.category}</p>
                                <h3 class="font-bold text-xl text-neutral-900 dark:text-white">${rec.name}</h3>
                            </div>
                        </div>
                        <p class="text-accent font-bold text-2xl">${rec.price}</p>
                        <a href="${rec.link}" class="block w-full mt-6 text-center bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 py-3 rounded-xl font-semibold hover:bg-accent hover:text-white transition-colors">
                            View Details & Price
                        </a>
                    </div>
                `).join('')}
            </div>
            <div class="text-center">
                <button onclick="startQuiz()" class="bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white border border-neutral-300 dark:border-neutral-700 px-10 py-4 rounded-2xl font-bold hover:shadow-xl transition-all mr-4">
                    <i class="fa-solid fa-rotate-left mr-2"></i> Retake Quiz
                </button>
                <a href="/deals/" class="bg-gradient-to-r from-primary to-accent text-white px-10 py-4 rounded-2xl font-bold hover:shadow-xl transition-all inline-block">
                    Browse All Products <i class="fa-solid fa-arrow-right ml-2"></i>
                </a>
            </div>
        </div>
    `;
}

// Initialize quiz on page load if quiz section exists
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('quiz-container')) {
        // Quiz is already pre‑rendered with start button
    }
});