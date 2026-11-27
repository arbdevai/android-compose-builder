package __PACKAGE__.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import __PACKAGE__.data.Product

@Composable
fun CartScreen(viewModel: KasirViewModel, modifier: Modifier = Modifier) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val cart by viewModel.cart.collectAsStateWithLifecycle()
    val message by viewModel.checkoutMessage.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(message) {
        if (message != null) {
            snackbarHostState.showSnackbar(message ?: "")
            viewModel.clearMessage()
        }
    }

    val cartProducts = uiState.products.filter { cart.containsKey(it.id) }
    val total = cartProducts.sumOf { product -> product.price * (cart[product.id] ?: 0) }

    Scaffold(
        modifier = modifier.fillMaxSize(),
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { innerPadding ->
        if (cartProducts.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize().padding(innerPadding),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "Keranjang masih kosong.", style = MaterialTheme.typography.bodyMedium)
            }
            return@Scaffold
        }
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding)) {
            LazyColumn(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(cartProducts, key = { it.id }) { product ->
                    CartRow(
                        product = product,
                        qty = cart[product.id] ?: 0,
                        onIncrease = { viewModel.addToCart(product) },
                        onDecrease = { viewModel.removeFromCart(product.id) }
                    )
                }
            }
            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(text = "Total", style = MaterialTheme.typography.titleMedium)
                    Text(text = formatRupiah(total), style = MaterialTheme.typography.titleMedium)
                }
                Button(
                    onClick = { viewModel.checkout() },
                    modifier = Modifier.fillMaxWidth().padding(top = 12.dp)
                ) {
                    Text(text = "Bayar ${formatRupiah(total)}")
                }
            }
        }
    }
}

@Composable
private fun CartRow(
    product: Product,
    qty: Int,
    onIncrease: () -> Unit,
    onDecrease: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = product.name, style = MaterialTheme.typography.titleMedium)
                Text(
                    text = "${formatRupiah(product.price)} x $qty = ${formatRupiah(product.price * qty)}",
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            IconButton(onClick = onDecrease) {
                Icon(Icons.Filled.Remove, contentDescription = "Kurangi jumlah")
            }
            Text(text = qty.toString(), style = MaterialTheme.typography.titleMedium)
            IconButton(onClick = onIncrease, enabled = qty < product.stock) {
                Icon(Icons.Filled.Add, contentDescription = "Tambah jumlah")
            }
        }
    }
}
