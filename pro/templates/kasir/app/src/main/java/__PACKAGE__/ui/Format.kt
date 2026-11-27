package __PACKAGE__.ui

import java.text.NumberFormat
import java.util.Locale

/** Format Rupiah tanpa desimal, contoh: Rp15.000 */
fun formatRupiah(amount: Long): String {
    val formatter = NumberFormat.getCurrencyInstance(Locale("id", "ID"))
    formatter.maximumFractionDigits = 0
    return formatter.format(amount)
}
