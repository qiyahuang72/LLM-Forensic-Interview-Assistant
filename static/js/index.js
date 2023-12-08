let consultingHistory = [];
consultingHistory.push({
    interview: "Q1: When was the last time you danced? A1: I don't know",
    suggestions: ["Can you think of a time when you danced?",
                ['Can you tell me about any time you remember dancing?', 
                "Can you think of any time recently when you were dancing?", 
                'Can you think of any time when you danced?', 
                'Can you think of any time recently when you danced or saw someone else dancing?']],
    promptType: "Chain of Thought",
    },
    {interview: "Q1: What fun was it to be in the park? A1: Everybody's terrible. It's awful.",
    suggestions: ["Why do you say it's awful?",
                ["Why do you think everybody was terrible at the park?",
                "What do you remember about being in the park?",
                "Why was everybody terrible in the park?",
                "Why do you think everyone was terrible at the park?"]],
    promptType: "In-context Learning",
    },
    {interview: "Q1: Can you tell me anything about Daddy? A1: Daddy bullied Yuzuki.",
    suggestions: ["What did Daddy do to Yuzuki",
                ["How did Daddy bully Yuzuki?"]],
    promptType: "In-context Learning",
    }
);


async function submitInterview() {
    const interviewHistory = document.getElementById('interviewHistory').value;
    const selectedPromptType = document.getElementById('promptType').value;

    const suggestionsDiv = document.getElementById('suggestions');
    suggestionsDiv.innerHTML = '<h2>Suggestions:</h2>';

    const response = await fetch('/generate_suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ interview_history: interviewHistory, prompt_type: selectedPromptType }),
    });

    const data = await response.json();
    console.log(data.suggestions[0])
    console.log(data.suggestions[1])

    consultingHistory.push({
        interview: interviewHistory,
        suggestions: data.suggestions,
        promptType: selectedPromptType,
    });
    console.log(consultingHistory)
    updateConsultingHistoryList();
    displayInterview(consultingHistory.length - 1)
}

function updateConsultingHistoryList() {
    const consultingHistoryList = document.getElementById('consultingHistoryList'); 
    consultingHistoryList.innerHTML = '';

    consultingHistory.forEach((consultation, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `Consultation ${index + 1}`;
        listItem.addEventListener('click', () => displayInterview(index));
        consultingHistoryList.appendChild(listItem);
    });
}

function displayInterview(index) {
    const interviewText = document.getElementById('interviewHistory');
    interviewText.value = consultingHistory[index].interview;
    const selectedPrompt = document.getElementById('promptType');
    selectedPrompt.value = consultingHistory[index].promptType;
    displaySuggestions(consultingHistory[index].suggestions);
}

function displaySuggestions(suggestions) {
    const suggestionsDiv = document.getElementById('suggestions');
    suggestionsDiv.innerHTML = '<h2>Suggestions:</h2>';
    
    // const suggestionElement = document.createElement('p');
    // suggestionElement.textContent = suggestions;
    // suggestionsDiv.appendChild(suggestionElement);

    const recommendedElement = document.createElement('p');
    recommendedElement.textContent = suggestions[0];
    suggestionsDiv.appendChild(recommendedElement);

    for (const option of suggestions[1]) {
        const optionElement = document.createElement('p');
        optionElement.textContent = option;
        suggestionsDiv.appendChild(optionElement);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateConsultingHistoryList();
});

//Q1: When was the last time you danced? A1: I don't know
