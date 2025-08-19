using System.Text.Json.Serialization;

namespace Neurons_Types
{
    // The response from the API/LLM
    public class ImageEvaluationResponse
    {
        [JsonPropertyName("prompt_used")]
        public string PromptUsed { get; set; } = "";

        [JsonPropertyName("model_output")]
        public string ModelOutput { get; set; } = "";
    }
    public class BrandComplianceResponse
    {
        public ComplianceRequirements Requirements { get; set; } = new();
        public string Message { get; set; } = "";
    }

    public class ComplianceRequirements
    {
        [JsonPropertyName("font_styles")]
        public Dictionary<string, string>? FontStyles { get; set; }

        [JsonPropertyName("logo_safezone")]
        public LogoSafezone? LogoSafezone { get; set; }

        [JsonPropertyName("logo_colour")]
        public LogoColour? LogoColour { get; set; }

        [JsonPropertyName("logo_colour_palette")]
        public LogoColourPalette? LogoColourPalette { get; set; }
    }

    public class LogoSafezone
    {
        public string? Value { get; set; }
        public string? Requirements { get; set; }
    }

    public class LogoColour
    {
        [JsonPropertyName("Logo colours")]
        public List<string>? LogoColours { get; set; }
    }

    public class LogoColourPalette
    {
        public List<string>? Colours { get; set; }
    }
}