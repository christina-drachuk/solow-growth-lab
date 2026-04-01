"""Tests for solow_growth/app.py — AI insight function (Gemini integration mocked)."""

from unittest.mock import patch, MagicMock

# Patch Streamlit before importing app to avoid runtime errors
import sys
from unittest.mock import MagicMock as _MagicMock

# Create a mock streamlit module that won't try to render UI
_mock_st = _MagicMock()
_mock_st.cache_data = lambda **kwargs: lambda f: f  # passthrough decorator


@patch.dict(sys.modules, {"streamlit": _mock_st})
def _import_get_ai_insight():
    """Import get_ai_insight while Streamlit is mocked."""
    # We need to also mock the top-level app module imports
    # that trigger Streamlit rendering calls
    import importlib
    import solow_growth.app as app_module

    return app_module.get_ai_insight


# ── get_ai_insight ──────────────────────────────────────────────────────


class TestGetAiInsight:
    """Tests for the Gemini-powered AI insight generator."""

    @patch("solow_growth.app.genai")
    def test_returns_response_text(self, mock_genai):
        """Should return the text from Gemini's response."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(
            text="• Insight 1\n• Insight 2\n• Insight 3"
        )
        mock_genai.GenerativeModel.return_value = mock_model

        from solow_growth.app import get_ai_insight

        result = get_ai_insight(
            s=0.20, n=0.02, g=0.02, delta=0.05,
            k_star=3.07, countries=["United States", "Japan"],
        )

        assert result == "• Insight 1\n• Insight 2\n• Insight 3"

    @patch("solow_growth.app.genai")
    def test_prompt_contains_parameters(self, mock_genai):
        """The prompt sent to Gemini should include all model parameters."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text="insights")
        mock_genai.GenerativeModel.return_value = mock_model

        from solow_growth.app import get_ai_insight

        get_ai_insight(
            s=0.20, n=0.02, g=0.02, delta=0.05,
            k_star=3.07, countries=["United States", "Germany"],
        )

        # Extract the prompt that was passed to generate_content
        call_args = mock_model.generate_content.call_args
        prompt = call_args[0][0]

        assert "0.2" in prompt
        assert "0.02" in prompt
        assert "0.05" in prompt
        assert "3.07" in prompt
        assert "United States" in prompt
        assert "Germany" in prompt

    @patch("solow_growth.app.genai")
    def test_configures_api_key(self, mock_genai):
        """Should call genai.configure with the API key."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text="insights")
        mock_genai.GenerativeModel.return_value = mock_model

        from solow_growth.app import get_ai_insight

        with patch.dict("os.environ", {"GOOGLE_API_KEY": "test-key-123"}):
            get_ai_insight(
                s=0.20, n=0.02, g=0.02, delta=0.05,
                k_star=3.07, countries=["Japan"],
            )

        mock_genai.configure.assert_called()
