using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

namespace STT_Application.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class TranscribeController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<TranscribeController> _logger;

        public TranscribeController(ILogger<TranscribeController> logger)
        {
            _logger = logger;
            PythonEngine.Initialize();
        }

        [HttpGet(Name = "Transcribe")]
        public string Get()
        {
            using (Py.GIL())
            {
                dynamic python = Py.Import("scripts/celery_worker");
                // dynamic result = python.trancribe_audio("123", "https://etrucknet.com/one.m4a");
                dynamic result = python.trancribe_audio("123", "https://etrucknet.com/two.m4a");
                return result;
            }

        }
    }
}
