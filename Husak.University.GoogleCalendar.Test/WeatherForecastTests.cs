using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Husak.University.GoogleCalendar.Core.Interfaces;
using Husak.University.GoogleCalendar.Models.Configuration;

namespace Husak.University.GoogleCalendar.Test
{
    [TestClass]
    public class WeatherForecastTests : TestBase
    {
        ILogger<WeatherForecastTests> _logger;
        IWeatherForecastService _weatherForecastService;
        IOptions<AppConfig> _configuration;

        public WeatherForecastTests()
        {
            _logger = ResolveService<ILogger<WeatherForecastTests>>();
            _weatherForecastService = ResolveService<IWeatherForecastService>();
            _configuration = ResolveService<IOptions<AppConfig>>();
        }

        [TestMethod]
        public void Get_Forecast_Should_Return_AmountOfResults_From_Config()
        {
            _logger.LogInformation($"Executing {nameof(Get_Forecast_Should_Return_AmountOfResults_From_Config)} method.");
            var forecast = _weatherForecastService.GetRandomForecast();
            Assert.AreEqual(forecast.Count(), _configuration?.Value?.ForecastAmount);
        }
    }
}