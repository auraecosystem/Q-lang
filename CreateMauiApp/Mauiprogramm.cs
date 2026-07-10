#if WINDOWS
    string relativePath = @"Runtime";
    string basePath = AppContext.BaseDirectory;
    string wvrPath = Path.Combine(basePath, relativePath);
    Environment.SetEnvironmentVariable("WEBVIEW2_BROWSER_EXECUTABLE_FOLDER", wvrPath);
#endif
