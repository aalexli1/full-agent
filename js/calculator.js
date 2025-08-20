/**
 * Calculator Application
 * A fully functional calculator with keyboard support and proper error handling
 */

class Calculator {
    constructor() {
        // State management
        this.currentInput = '0';
        this.previousInput = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.expression = '';
        
        // DOM elements
        this.resultDisplay = document.getElementById('result');
        this.expressionDisplay = document.getElementById('expression');
        
        // Initialize event listeners
        this.initializeEventListeners();
        this.updateDisplay();
    }

    /**
     * Initialize all event listeners for buttons and keyboard
     */
    initializeEventListeners() {
        // Button event listeners
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleButtonClick(e.target);
                this.animateButton(e.target);
            });
        });

        // Keyboard event listeners
        document.addEventListener('keydown', (e) => {
            this.handleKeyPress(e);
        });
    }

    /**
     * Handle button clicks
     */
    handleButtonClick(button) {
        const action = button.dataset.action;
        const number = button.dataset.number;
        const operator = button.dataset.operator;

        if (number !== undefined) {
            this.inputNumber(number);
        } else if (operator) {
            this.inputOperator(operator);
        } else if (action) {
            this.performAction(action);
        }
    }

    /**
     * Handle keyboard input
     */
    handleKeyPress(event) {
        const key = event.key;
        
        // Prevent default for calculator keys
        if (/[0-9+\-*/.=]|Enter|Backspace|Escape|Delete/.test(key)) {
            event.preventDefault();
        }

        // Number keys
        if (/[0-9.]/.test(key)) {
            this.inputNumber(key);
        }
        // Operator keys
        else if (key === '+') {
            this.inputOperator('+');
        } else if (key === '-') {
            this.inputOperator('-');
        } else if (key === '*') {
            this.inputOperator('*');
        } else if (key === '/') {
            this.inputOperator('/');
        }
        // Action keys
        else if (key === 'Enter' || key === '=') {
            this.performAction('equals');
        } else if (key === 'Backspace' || key === 'Delete') {
            this.performAction('backspace');
        } else if (key === 'Escape') {
            this.performAction('clear');
        } else if (key === '%') {
            this.performAction('percent');
        }

        // Find and animate corresponding button
        this.animateCorrespondingButton(key);
    }

    /**
     * Input a number or decimal point
     */
    inputNumber(num) {
        if (num === '.') {
            // Prevent multiple decimal points
            if (this.currentInput.includes('.')) {
                return;
            }
            // Add leading zero if starting with decimal
            if (this.waitingForOperand || this.currentInput === '0') {
                this.currentInput = '0.';
            } else {
                this.currentInput += '.';
            }
        } else {
            if (this.waitingForOperand) {
                this.currentInput = num;
                this.waitingForOperand = false;
            } else {
                this.currentInput = this.currentInput === '0' ? num : this.currentInput + num;
            }
        }

        this.updateDisplay();
    }

    /**
     * Input an operator
     */
    inputOperator(nextOperator) {
        const inputValue = parseFloat(this.currentInput);

        if (this.previousInput === null) {
            this.previousInput = inputValue;
        } else if (this.operator) {
            const currentValue = this.previousInput || 0;
            const newValue = this.calculate(currentValue, inputValue, this.operator);

            if (newValue === null) return; // Error occurred

            this.currentInput = String(newValue);
            this.previousInput = newValue;
            this.updateDisplay();
        }

        this.waitingForOperand = true;
        this.operator = nextOperator;
        this.updateExpression();
        this.highlightOperator(nextOperator);
    }

    /**
     * Perform calculator actions
     */
    performAction(action) {
        switch (action) {
            case 'clear':
                this.clear();
                break;
            case 'backspace':
                this.backspace();
                break;
            case 'equals':
                this.equals();
                break;
            case 'percent':
                this.percent();
                break;
        }
    }

    /**
     * Calculate result based on operator
     */
    calculate(firstOperand, secondOperand, operator) {
        switch (operator) {
            case '+':
                return this.roundResult(firstOperand + secondOperand);
            case '-':
                return this.roundResult(firstOperand - secondOperand);
            case '*':
                return this.roundResult(firstOperand * secondOperand);
            case '/':
                if (secondOperand === 0) {
                    this.showError('Cannot divide by zero');
                    return null;
                }
                return this.roundResult(firstOperand / secondOperand);
            default:
                return secondOperand;
        }
    }

    /**
     * Round result to handle floating point precision issues
     */
    roundResult(result) {
        // Handle floating point precision issues (like 0.1 + 0.2)
        return Math.round(result * 1000000000000) / 1000000000000;
    }

    /**
     * Clear calculator
     */
    clear() {
        this.currentInput = '0';
        this.previousInput = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.expression = '';
        this.clearHighlight();
        this.updateDisplay();
    }

    /**
     * Backspace functionality
     */
    backspace() {
        if (this.currentInput.length > 1) {
            this.currentInput = this.currentInput.slice(0, -1);
        } else {
            this.currentInput = '0';
        }
        this.updateDisplay();
    }

    /**
     * Equals functionality
     */
    equals() {
        const inputValue = parseFloat(this.currentInput);

        if (this.previousInput !== null && this.operator) {
            const newValue = this.calculate(this.previousInput, inputValue, this.operator);
            
            if (newValue === null) return; // Error occurred

            // Update expression to show the complete calculation
            this.expression = `${this.previousInput} ${this.getOperatorSymbol(this.operator)} ${inputValue} =`;
            
            this.currentInput = String(newValue);
            this.previousInput = null;
            this.operator = null;
            this.waitingForOperand = true;
            this.clearHighlight();
            this.updateDisplay();
        }
    }

    /**
     * Percent functionality
     */
    percent() {
        const inputValue = parseFloat(this.currentInput);
        this.currentInput = String(inputValue / 100);
        this.updateDisplay();
    }

    /**
     * Update the display
     */
    updateDisplay() {
        // Format the result display
        const displayValue = this.formatNumber(this.currentInput);
        this.resultDisplay.textContent = displayValue;
        
        // Update expression display
        this.expressionDisplay.textContent = this.expression;
        
        // Auto-resize text if too long
        this.adjustFontSize();
    }

    /**
     * Update expression display
     */
    updateExpression() {
        if (this.previousInput !== null && this.operator) {
            this.expression = `${this.previousInput} ${this.getOperatorSymbol(this.operator)}`;
        }
    }

    /**
     * Format number for display
     */
    formatNumber(num) {
        const number = parseFloat(num);
        
        // Handle very large numbers with scientific notation
        if (Math.abs(number) >= 1e9) {
            return number.toExponential(5);
        }
        
        // Handle very small numbers
        if (Math.abs(number) < 1e-6 && number !== 0) {
            return number.toExponential(5);
        }
        
        // Regular formatting
        const formatted = number.toLocaleString('en-US', {
            maximumFractionDigits: 10,
            useGrouping: false
        });
        
        return formatted;
    }

    /**
     * Get operator symbol for display
     */
    getOperatorSymbol(operator) {
        const symbols = {
            '+': '+',
            '-': '',
            '*': '×',
            '/': '÷'
        };
        return symbols[operator] || operator;
    }

    /**
     * Highlight active operator
     */
    highlightOperator(operator) {
        this.clearHighlight();
        const operatorButton = document.querySelector(`[data-operator="${operator}"]`);
        if (operatorButton) {
            operatorButton.classList.add('active');
        }
    }

    /**
     * Clear operator highlight
     */
    clearHighlight() {
        document.querySelectorAll('.btn-operator').forEach(btn => {
            btn.classList.remove('active');
        });
    }

    /**
     * Show error message
     */
    showError(message) {
        this.resultDisplay.textContent = 'Error';
        this.expressionDisplay.textContent = message;
        
        // Clear error after 3 seconds
        setTimeout(() => {
            this.clear();
        }, 3000);
    }

    /**
     * Adjust font size for long numbers
     */
    adjustFontSize() {
        const length = this.resultDisplay.textContent.length;
        const display = this.resultDisplay;
        
        if (length > 12) {
            display.style.fontSize = '32px';
        } else if (length > 8) {
            display.style.fontSize = '40px';
        } else {
            display.style.fontSize = '48px';
        }
    }

    /**
     * Animate button press
     */
    animateButton(button) {
        button.classList.add('animate');
        setTimeout(() => {
            button.classList.remove('animate');
        }, 200);
    }

    /**
     * Animate button corresponding to keyboard press
     */
    animateCorrespondingButton(key) {
        let selector = '';
        
        if (/[0-9]/.test(key)) {
            selector = `[data-number="${key}"]`;
        } else if (key === '.') {
            selector = '[data-number="."]';
        } else if (key === '+') {
            selector = '[data-operator="+"]';
        } else if (key === '-') {
            selector = '[data-operator="-"]';
        } else if (key === '*') {
            selector = '[data-operator="*"]';
        } else if (key === '/') {
            selector = '[data-operator="/"]';
        } else if (key === 'Enter' || key === '=') {
            selector = '[data-action="equals"]';
        } else if (key === 'Backspace' || key === 'Delete') {
            selector = '[data-action="backspace"]';
        } else if (key === 'Escape') {
            selector = '[data-action="clear"]';
        } else if (key === '%') {
            selector = '[data-action="percent"]';
        }

        if (selector) {
            const button = document.querySelector(selector);
            if (button) {
                this.animateButton(button);
            }
        }
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Calculator();
});

// Handle page visibility changes to prevent issues with suspended calculations
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Clear any pending operations when page is hidden
        return;
    }
});