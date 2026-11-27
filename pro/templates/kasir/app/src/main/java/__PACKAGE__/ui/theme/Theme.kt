package __PACKAGE__.ui.theme

import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Skala netral murni (R=G=B) sesuai aturan anti-AI-slop skill. Tanpa navy kebiruan.
private val NeutralBlack = Color(0xFF000000)
private val NeutralDark = Color(0xFF121212)
private val NeutralSurface = Color(0xFF1E1E1E)
private val NeutralSurfaceHigh = Color(0xFF242424)
private val NeutralOnDark = Color(0xFFF5F5F5)
private val NeutralMuted = Color(0xFF9E9E9E)
private val AccentGreen = Color(0xFF2E7D32)

private val DarkColors = darkColorScheme(
    primary = AccentGreen,
    background = NeutralDark,
    surface = NeutralSurface,
    surfaceVariant = NeutralSurfaceHigh,
    onBackground = NeutralOnDark,
    onSurface = NeutralOnDark,
    onSurfaceVariant = NeutralMuted
)

private val LightColors = lightColorScheme(
    primary = AccentGreen,
    background = Color(0xFFFAFAFA),
    surface = Color(0xFFFFFFFF),
    surfaceVariant = Color(0xFFEEEEEE),
    onBackground = Color(0xFF121212),
    onSurface = Color(0xFF121212),
    onSurfaceVariant = Color(0xFF616161)
)

@Composable
fun KasirTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        typography = Typography(),
        content = content
    )
}
