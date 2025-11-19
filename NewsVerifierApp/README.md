# News Verifier Android App

Complete Android application for verifying news using AI.

## 🚀 Quick Start

### Prerequisites
- Android Studio (latest version)
- JDK 8 or higher
- Android SDK with API 24 or higher

### Setup Instructions

1. **Open in Android Studio**
   - Launch Android Studio
   - Select "Open an Existing Project"
   - Navigate to this folder and click OK

2. **Sync Gradle**
   - Wait for Gradle sync to complete
   - If prompted, click "Sync Now"

3. **Configure Backend URL**
   - Open `app/src/main/java/com/newsverifier/api/RetrofitClient.kt`
   - Update `BASE_URL`:
     - For Emulator: `http://10.0.2.2:8000/` (localhost)
     - For Physical Device: `http://YOUR_COMPUTER_IP:8000/`

4. **Run the App**
   - Connect Android device or start emulator
   - Click Run (green play button) or press Shift+F10
   - Select your device
   - App will install and launch

## 📱 Features

- ✅ News verification using AI
- ✅ Support for text and URL input
- ✅ Confidence score display
- ✅ Evidence source links
- ✅ Material Design 3 UI
- ✅ Real-time API health check
- ✅ MVVM architecture

## 🏗️ Project Structure

```
app/
├── src/main/
│   ├── java/com/newsverifier/
│   │   ├── api/              # Retrofit API interfaces
│   │   ├── models/           # Data models
│   │   ├── repository/       # Data repository
│   │   ├── ui/              # Activities
│   │   └── viewmodel/       # ViewModels
│   ├── res/                 # Resources (layouts, strings, etc.)
│   └── AndroidManifest.xml
└── build.gradle.kts
```

## 🔧 Configuration

### API Endpoint
Edit `RetrofitClient.kt` to change the backend URL.

### Dependencies
All dependencies are configured in `app/build.gradle.kts`:
- Retrofit 2.9.0
- Material Components 1.11.0
- Coroutines 1.7.3
- ViewModel & LiveData

## 📝 Build Variants

- **Debug**: Development build with logging
- **Release**: Production build (requires signing)

## 🐛 Troubleshooting

**API Connection Failed:**
- Ensure backend is running on http://localhost:8000
- For emulator, use `10.0.2.2` instead of `localhost`
- For physical device, use computer's IP address
- Check firewall settings

**Gradle Sync Failed:**
- File → Invalidate Caches → Invalidate and Restart
- Check internet connection
- Update Android Studio to latest version

**App Crashes:**
- Check Logcat for error messages
- Verify all permissions in AndroidManifest.xml
- Ensure internet permission is granted

## 📦 Building APK

**Debug APK:**
```
./gradlew assembleDebug
```

**Release APK:**
```
./gradlew assembleRelease
```

APK location: `app/build/outputs/apk/`

## 🔐 Permissions Required

- `INTERNET` - For API calls
- `ACCESS_NETWORK_STATE` - Check network connectivity

## 📄 License

This project is part of the News Verification AI system.
