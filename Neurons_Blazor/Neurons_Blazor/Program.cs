using Neurons_Blazor.Components;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);

// Pick from env var first (Docker), fall back to local dev
var apiBase = Environment.GetEnvironmentVariable("API_BASE_URL")
              ?? "http://localhost:8000/"; // dev when running API locally

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddMudServices();
// Named client you can inject everywhere
builder.Services.AddHttpClient("Api", c => c.BaseAddress = new Uri(apiBase));


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
