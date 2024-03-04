using Husak.University.GoogleCalendar.Models.Weather;

namespace Husak.University.GoogleCalendar.Core.Interfaces
{
    public interface IWeatherForecastService
    {
        IEnumerable<WeatherForecast> GetRandomForecast();
    }
}
