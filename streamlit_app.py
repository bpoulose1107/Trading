{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "377246c3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: streamlit in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (1.47.0)\n",
      "Requirement already satisfied: altair<6,>=4.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (5.5.0)\n",
      "Requirement already satisfied: blinker<2,>=1.5.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (1.9.0)\n",
      "Requirement already satisfied: cachetools<7,>=4.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (5.5.2)\n",
      "Requirement already satisfied: click<9,>=7.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (8.2.1)\n",
      "Requirement already satisfied: numpy<3,>=1.23 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (2.2.6)\n",
      "Requirement already satisfied: packaging<26,>=20 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (25.0)\n",
      "Requirement already satisfied: pandas<3,>=1.4.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (2.3.0)\n",
      "Requirement already satisfied: pillow<12,>=7.1.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (11.2.1)\n",
      "Requirement already satisfied: protobuf<7,>=3.20 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (6.31.1)\n",
      "Requirement already satisfied: pyarrow>=7.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (20.0.0)\n",
      "Requirement already satisfied: requests<3,>=2.27 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (2.32.4)\n",
      "Requirement already satisfied: tenacity<10,>=8.1.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (9.1.2)\n",
      "Requirement already satisfied: toml<2,>=0.10.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.4.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (4.14.1)\n",
      "Requirement already satisfied: watchdog<7,>=2.1.5 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (6.0.0)\n",
      "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (3.1.45)\n",
      "Requirement already satisfied: pydeck<1,>=0.8.0b4 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (0.9.1)\n",
      "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from streamlit) (6.5.1)\n",
      "Requirement already satisfied: jinja2 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from altair<6,>=4.0->streamlit) (3.1.6)\n",
      "Requirement already satisfied: jsonschema>=3.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from altair<6,>=4.0->streamlit) (4.25.0)\n",
      "Requirement already satisfied: narwhals>=1.14.2 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from altair<6,>=4.0->streamlit) (1.48.0)\n",
      "Requirement already satisfied: colorama in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from click<9,>=7.0->streamlit) (0.4.6)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests<3,>=2.27->streamlit) (3.4.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests<3,>=2.27->streamlit) (2025.7.14)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
      "Requirement already satisfied: attrs>=22.2.0 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (25.3.0)\n",
      "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2025.4.1)\n",
      "Requirement already satisfied: referencing>=0.28.4 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.36.2)\n",
      "Requirement already satisfied: rpds-py>=0.7.1 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.26.0)\n",
      "Requirement already satisfied: six>=1.5 in c:\\users\\biss\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "[notice] A new release of pip available: 22.3.1 -> 25.2\n",
      "[notice] To update, run: C:\\Users\\BISS\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m pip install --upgrade pip\n"
     ]
    }
   ],
   "source": [
    "!pip install streamlit\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "50aa845a",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'streamlit'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[4], line 1\u001b[0m\n\u001b[1;32m----> 1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mstreamlit\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mst\u001b[39;00m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mpandas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mpd\u001b[39;00m\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mmatplotlib\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mpyplot\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mplt\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Load logged data (assumes saved as CSV)\n",
    "@st.cache_data\n",
    "def load_log():\n",
    "    return pd.read_csv(\"action_log.csv\")\n",
    "\n",
    "st.set_page_config(layout=\"wide\")\n",
    "st.title(\"📈 DRL Trading Agent Dashboard\")\n",
    "\n",
    "# Load and show the data\n",
    "log_df = load_log()\n",
    "st.subheader(\"Sample of Agent Actions\")\n",
    "st.dataframe(log_df.tail(10))\n",
    "\n",
    "# Plot cumulative reward\n",
    "log_df[\"Cumulative_Reward\"] = log_df[\"Reward\"].cumsum()\n",
    "fig, ax = plt.subplots()\n",
    "ax.plot(log_df[\"Step\"], log_df[\"Cumulative_Reward\"])\n",
    "ax.set_title(\"Cumulative Reward Over Time\")\n",
    "ax.set_xlabel(\"Step\")\n",
    "ax.set_ylabel(\"Cumulative Reward\")\n",
    "st.pyplot(fig)\n",
    "\n",
    "# Show action breakdown\n",
    "st.subheader(\"Action Distribution\")\n",
    "st.write(\"BTC Actions:\")\n",
    "st.bar_chart(log_df[\"BTC_action\"].value_counts())\n",
    "st.write(\"S&P500 Actions:\")\n",
    "st.bar_chart(log_df[\"SP500_action\"].value_counts())\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
