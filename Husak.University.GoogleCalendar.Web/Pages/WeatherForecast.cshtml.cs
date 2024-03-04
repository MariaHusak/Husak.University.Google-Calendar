using Microsoft.AspNetCore.Mvc.RazorPages;
using Husak.University.GoogleCalendar.Core.Interfaces;
using Husak.University.GoogleCalendar.Models.Weather;

namespace Husak.University.GoogleCalendar.Web.Pages
{
    public class WeatherForecastModel : PageModel
    {
        public IList<WeatherForecast> Forecasts { get; set; }

        private readonly IWeatherForecastService _weatherForecastService;

        public WeatherForecastModel(IWeatherForecastService weatherForecastService)
        {
            _weatherForecastService = weatherForecastService;
        }

        public void OnGet()
        {
            Forecasts = _weatherForecastService.GetRandomForecast().ToList();
        }
    }
}