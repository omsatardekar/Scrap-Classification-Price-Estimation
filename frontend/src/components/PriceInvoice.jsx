export default function PriceInvoice({
  price,
  breakdown,
  show,
  onToggle,
}) {
  if (price === null) return null;

  return (
    <div className="relative max-w-3xl mx-auto">

      {/* INVOICE CARD */}
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-xl">

        {/* HEADER */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white">
              AI Price Estimation
            </h3>
            <p className="text-sm text-gray-400">
              Generated using ScrapX pricing engine
            </p>
          </div>

          <span className="material-icons-outlined text-cyan-400 text-3xl">
            receipt_long
          </span>
        </div>

        {/* PRICE */}
        <div className="text-center py-8 border-y border-white/10 mb-6">
          <p className="text-sm text-gray-400 mb-2">
            Estimated Scrap Value
          </p>
          <p className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-400">
            ₹ {price}
          </p>
        </div>

        {/* TOGGLE */}
        {breakdown && (
          <button
            onClick={onToggle}
            className="flex items-center gap-2 mx-auto text-sm text-cyan-400 hover:text-cyan-300 transition"
          >
            <span className="material-icons-outlined text-base">
              {show ? "expand_less" : "expand_more"}
            </span>
            {show ? "Hide price breakdown" : "View detailed breakdown"}
          </button>
        )}

        {/* BREAKDOWN */}
        {show && breakdown && (
          <div className="mt-8 bg-black/40 rounded-2xl border border-white/10 overflow-hidden">

            {/* TABLE HEADER */}
            <div className="grid grid-cols-3 px-5 py-3 text-xs uppercase tracking-wide text-gray-400 border-b border-white/10">
              <span>Component</span>
              <span className="text-center">Details</span>
              <span className="text-right">Amount</span>
            </div>

            {/* ROWS */}
            {breakdown.map((item, idx) => (
              <div
                key={idx}
                className="grid grid-cols-3 px-5 py-4 border-b border-white/5 last:border-none"
              >
                <div>
                  <p className="text-sm font-medium text-white">
                    {item.label}
                  </p>
                </div>

                <div className="text-center text-xs text-gray-400">
                  {item.value}
                </div>

                <div className="text-right font-semibold text-white">
                  ₹ {item.amount}
                </div>
              </div>
            ))}

            {/* TOTAL */}
            <div className="grid grid-cols-3 px-5 py-4 bg-white/5 font-semibold">
              <span className="text-green-400">
                Total Estimated Price
              </span>
              <span></span>
              <span className="text-right text-green-400">
                ₹ {price}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
