import sys

theme = 'dark'
toggle_off_bg = '#C7C7CC' if theme == 'light' else '#48484A'

base_css = f"""
    <style>
    /* Premium Typography & Header */
    .premium-title {{
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFD700 0%, #D4AF37 50%, #8B6508 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }}
    
    /* iOS 26 Toggles Perfected */
    [data-testid="stToggle"] [data-baseweb="checkbox"],
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] {{
        min-height: 40px !important;
        display: flex !important;
        align-items: center !important;
        margin-bottom: 12px !important;
        width: 100% !important;
    }}

    [data-testid="stToggle"] [data-baseweb="checkbox"] > input + div,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input + div {{
        width: 51px !important;
        height: 31px !important;
        border-radius: 31px !important;
        padding: 2px !important;
        box-sizing: border-box !important;
        background-color: {toggle_off_bg} !important;
        border: none !important;
        transition: background-color 0.4s cubic-bezier(0.25, 0.1, 0.25, 1) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        position: relative !important;
        flex-shrink: 0 !important;
    }}
    
    [data-testid="stToggle"] [data-baseweb="checkbox"] > input + div > div,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input + div > div {{
        width: 27px !important;
        height: 27px !important;
        border-radius: 50% !important;
        background-color: #FFFFFF !important;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.15), 0px 3px 1px rgba(0,0,0,0.06) !important;
        transform: translateX(0px) !important;
        transition: transform 0.4s cubic-bezier(0.25, 0.1, 0.25, 1) !important;
        margin: 0 !important;
        position: absolute !important;
        left: 2px !important;
    }}
    
    [data-testid="stToggle"] [data-baseweb="checkbox"] > input:checked + div,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input:checked + div {{
        background-color: #D4AF37 !important; /* Gold */
    }}
    
    [data-testid="stToggle"] [data-baseweb="checkbox"] > input:checked + div > div,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input:checked + div > div {{
        transform: translateX(20px) !important;
    }}

    /* Предотвращаем любые фоновые заливки, смещения и перенос текста */
    [data-testid="stToggle"] [data-baseweb="checkbox"] > input + div + div,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input + div + div {{
        background-color: transparent !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        width: auto !important;
        min-width: max-content !important;
        margin-left: 12px !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    [data-testid="stToggle"] [data-baseweb="checkbox"] > input + div + div *,
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] > input + div + div * {{
        background-color: transparent !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        width: auto !important;
        min-width: max-content !important;
    }}
    </style>
"""

print(base_css)
