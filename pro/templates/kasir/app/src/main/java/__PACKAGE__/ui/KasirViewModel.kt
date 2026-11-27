package __PACKAGE__.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import __PACKAGE__.data.KasirRepository
import __PACKAGE__.data.Product
import __PACKAGE__.data.Sale
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class KasirUiState(
    val products: List<Product> = emptyList(),
    val sales: List<Sale> = emptyList(),
    val totalRevenue: Long = 0L,
    val isLoading: Boolean = true
)

class KasirViewModel(private val repository: KasirRepository) : ViewModel() {

    val uiState: StateFlow<KasirUiState> = kotlinx.coroutines.flow.combine(
        repository.observeProducts(),
        repository.observeSales(),
        repository.observeTotalRevenue()
    ) { products, sales, revenue ->
        KasirUiState(products = products, sales = sales, totalRevenue = revenue, isLoading = false)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), KasirUiState())

    // Keranjang: productId -> qty
    private val _cart = MutableStateFlow<Map<Long, Int>>(emptyMap())
    val cart: StateFlow<Map<Long, Int>> = _cart.asStateFlow()

    private val _checkoutMessage = MutableStateFlow<String?>(null)
    val checkoutMessage: StateFlow<String?> = _checkoutMessage.asStateFlow()

    fun addToCart(product: Product) {
        if (product.stock <= 0) return
        val current = _cart.value[product.id] ?: 0
        if (current >= product.stock) return
        _cart.value = _cart.value + (product.id to (current + 1))
    }

    fun removeFromCart(productId: Long) {
        val current = _cart.value[productId] ?: return
        _cart.value = if (current <= 1) {
            _cart.value - productId
        } else {
            _cart.value + (productId to (current - 1))
        }
    }

    fun clearCart() {
        _cart.value = emptyMap()
    }

    fun addProduct(name: String, price: Long, stock: Int) {
        viewModelScope.launch {
            runCatching { repository.addProduct(name, price, stock) }
                .onFailure { _checkoutMessage.value = it.message ?: "Gagal menambah produk" }
        }
    }

    fun deleteProduct(id: Long) {
        viewModelScope.launch { repository.deleteProduct(id) }
    }

    fun checkout() {
        val cart = _cart.value
        if (cart.isEmpty()) {
            _checkoutMessage.value = "Keranjang masih kosong"
            return
        }
        viewModelScope.launch {
            val saleId = repository.checkout(cart, uiState.value.products)
            if (saleId > 0) {
                _cart.value = emptyMap()
                _checkoutMessage.value = "Transaksi berhasil"
            } else {
                _checkoutMessage.value = "Gagal: stok tidak mencukupi"
            }
        }
    }

    fun clearMessage() {
        _checkoutMessage.value = null
    }
}
