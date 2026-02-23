export default function Features() {
  return (
    <div className="relative min-h-screen bg-[#0b0f1a] text-white overflow-hidden">

      {/* BACKGROUND GLOWS */}
      <div className="absolute -top-40 -right-40 w-[420px] h-[420px] bg-blue-600/20 blur-[140px] rounded-full" />
      <div className="absolute bottom-[-200px] left-[-200px] w-[420px] h-[420px] bg-cyan-500/20 blur-[140px] rounded-full" />

      {/* HERO */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-16 text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-6">
          Powerful Features
          <br />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400">
            Built for Smart Scrap Trading
          </span>
        </h1>

        <p className="max-w-3xl mx-auto text-gray-400 text-lg">
          ScrapX combines artificial intelligence, smart logistics, and
          digital systems to deliver a transparent and efficient scrap
          recycling experience.
        </p>
      </section>

      {/* CORE FEATURES GRID */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-10">
          {[
            {
              icon: "visibility",
              title: "AI Scrap Identification",
              desc: "Computer vision models analyze scrap images to identify material types accurately.",
            },
            {
              icon: "trending_up",
              title: "Intelligent Price Estimation",
              desc: "Machine learning algorithms estimate fair market prices based on material and weight.",
            },
            {
              icon: "dashboard",
              title: "Role-Based Dashboards",
              desc: "Dedicated dashboards for users, admins, and delivery agents with controlled access.",
            },
            {
              icon: "location_on",
              title: "Smart Pickup Assignment",
              desc: "Delivery agents are assigned automatically based on real-time location proximity.",
            },
            {
              icon: "verified",
              title: "Admin Verification",
              desc: "Admins verify scrap quality and pricing before final approval and pickup.",
            },
            {
              icon: "payments",
              title: "Secure Payment Simulation",
              desc: "End-to-end transaction flow with sandbox-based digital payment simulation.",
            },
          ].map((feature, i) => (
            <div
              key={i}
              className="group bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 hover:border-cyan-400 transition-all hover:-translate-y-2"
            >
              <span className="material-icons-outlined text-4xl text-cyan-400 mb-4 block">
                {feature.icon}
              </span>

              <h3 className="text-xl font-semibold mb-3">
                {feature.title}
              </h3>

              <p className="text-gray-400 text-sm leading-relaxed">
                {feature.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* FEATURE FLOW */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-24">
        <h2 className="text-4xl font-bold text-center mb-16">
          End-to-End Smart Workflow
        </h2>

        <div className="grid md:grid-cols-4 gap-8">
          {[
            { icon: "photo_camera", label: "Upload Scrap" },
            { icon: "psychology", label: "AI Analysis" },
            { icon: "local_shipping", label: "Smart Pickup" },
            { icon: "paid", label: "Digital Payout" },
          ].map((step, i) => (
            <div
              key={i}
              className="flex flex-col items-center text-center bg-white/5 border border-white/10 rounded-xl p-6 hover:border-cyan-400 transition"
            >
              <span className="material-icons-outlined text-5xl text-cyan-400 mb-4">
                {step.icon}
              </span>
              <span className="text-gray-300 font-medium">
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* WHY SCRAPX */}
      <section className="relative z-10 max-w-5xl mx-auto px-6 pb-20 text-center">
        <h2 className="text-3xl font-bold mb-4">
          Why ScrapX?
        </h2>
        <p className="text-gray-400 leading-relaxed">
          ScrapX is designed not just as a project, but as a scalable platform
          that demonstrates applied artificial intelligence, full-stack system
          design, and real-world problem solving.
        </p>
      </section>

      {/* FOOTER */}
      <footer className="relative z-10 py-8 text-center text-gray-500 text-sm border-t border-white/10">
        © {new Date().getFullYear()} ScrapX • Smart AI Scrap Platform
      </footer>
    </div>
  );
}
