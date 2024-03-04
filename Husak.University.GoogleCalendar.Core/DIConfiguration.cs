using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Husak.University.GoogleCalendar.Core.Interfaces;
using Husak.University.GoogleCalendar.Core.Services;
using Husak.University.GoogleCalendar.Models.Configuration;

namespace Husak.University.GoogleCalendar.Core
{
    public static class DIConfiguration
    {
        public static void RegisterCoreDependencies(this IServiceCollection services)
        {
            services.AddTransient<IWeatherForecastService, WeatherForecastService>();
        }

        public static void RegisterCoreConfiguration(this IServiceCollection services, IConfigurationRoot configuration)
        {
            services.Configure<AppConfig>(configuration.GetSection("AppConfig"));
        }
    }
}
