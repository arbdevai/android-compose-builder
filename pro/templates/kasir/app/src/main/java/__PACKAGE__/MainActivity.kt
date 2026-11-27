package __PACKAGE__

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Store
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import __PACKAGE__.data.KasirDatabase
import __PACKAGE__.data.KasirRepository
import __PACKAGE__.ui.CartScreen
import __PACKAGE__.ui.HistoryScreen
import __PACKAGE__.ui.KasirViewModel
import __PACKAGE__.ui.ProductsScreen
import __PACKAGE__.ui.theme.KasirTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val repository = KasirRepository(KasirDatabase.getInstance(applicationContext).kasirDao())
        setContent {
            KasirTheme {
                KasirApp(repository = repository)
            }
        }
    }
}

private object Routes {
    const val PRODUCTS = "products"
    const val CART = "cart"
    const val HISTORY = "history"
}

@Composable
fun KasirApp(repository: KasirRepository) {
    val navController = rememberNavController()
    val viewModel: KasirViewModel = viewModel(
        factory = object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return KasirViewModel(repository) as T
            }
        }
    )
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = backStackEntry?.destination?.route

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = currentRoute == Routes.PRODUCTS,
                    onClick = { navController.navigate(Routes.PRODUCTS) },
                    icon = { Icon(Icons.Filled.Store, contentDescription = "Produk") },
                    label = { Text(text = "Produk") }
                )
                NavigationBarItem(
                    selected = currentRoute == Routes.CART,
                    onClick = { navController.navigate(Routes.CART) },
                    icon = { Icon(Icons.Filled.ShoppingCart, contentDescription = "Keranjang") },
                    label = { Text(text = "Keranjang") }
                )
                NavigationBarItem(
                    selected = currentRoute == Routes.HISTORY,
                    onClick = { navController.navigate(Routes.HISTORY) },
                    icon = { Icon(Icons.Filled.History, contentDescription = "Riwayat") },
                    label = { Text(text = "Riwayat") }
                )
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Routes.PRODUCTS,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Routes.PRODUCTS) { ProductsScreen(viewModel = viewModel) }
            composable(Routes.CART) { CartScreen(viewModel = viewModel) }
            composable(Routes.HISTORY) { HistoryScreen(viewModel = viewModel) }
        }
    }
}
