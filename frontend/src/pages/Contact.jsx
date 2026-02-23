export default function Contact() {
  return (
    <div className="relative min-h-screen bg-[#0b0f1a] text-white overflow-hidden">

      {/* BACKGROUND GLOWS */}
      <div className="absolute -top-40 -right-40 w-[420px] h-[420px] bg-blue-600/20 blur-[140px] rounded-full" />
      <div className="absolute bottom-[-200px] left-[-200px] w-[420px] h-[420px] bg-cyan-500/20 blur-[140px] rounded-full" />

      {/* HERO */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-16 text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-6">
          Get in Touch
          <br />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400">
            with the ScrapX Team
          </span>
        </h1>

        <p className="max-w-3xl mx-auto text-gray-400 text-lg">
          Have questions about ScrapX, the technology behind it, or the system
          design? Reach out to us using the details below.
        </p>
      </section>

      {/* CONTACT CONTENT */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-12">

        {/* CONTACT INFO */}
        <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-6">
            Contact Information
          </h2>

          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <span className="material-icons-outlined text-cyan-400">
                email
              </span>
              <span className="text-gray-300">
                scrapx.project@gmail.com
              </span>
            </div>

            <div className="flex items-center gap-4">
              <span className="material-icons-outlined text-cyan-400">
                location_on
              </span>
              <span className="text-gray-300">
                University / College Campus, India
              </span>
            </div>

            <div className="flex items-center gap-4">
              <span className="material-icons-outlined text-cyan-400">
                school
              </span>
              <span className="text-gray-300">
                Final Year Engineering Project
              </span>
            </div>
          </div>

          <div className="mt-10 pt-6 border-t border-white/10 text-sm text-gray-400">
            This platform is developed as an academic project focusing on
            real-world application of artificial intelligence and system design.
          </div>
        </div>

        {/* MESSAGE FORM (OPTIONAL DEMO) */}
        <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-6">
            Send a Message
          </h2>

          <form className="space-y-5">
            <input
              type="text"
              placeholder="Your Name"
              className="w-full bg-transparent border border-white/10 rounded-lg px-4 py-3 text-gray-300 focus:outline-none focus:border-cyan-400"
            />

            <input
              type="email"
              placeholder="Your Email"
              className="w-full bg-transparent border border-white/10 rounded-lg px-4 py-3 text-gray-300 focus:outline-none focus:border-cyan-400"
            />

            <textarea
              rows="4"
              placeholder="Your Message"
              className="w-full bg-transparent border border-white/10 rounded-lg px-4 py-3 text-gray-300 focus:outline-none focus:border-cyan-400"
            />

            <button
              type="button"
              className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 font-semibold hover:opacity-90 transition"
            >
              <span className="material-icons-outlined">
                send
              </span>
              Send Message
            </button>
          </form>

          <p className="mt-4 text-xs text-gray-500">
            *Message submission is for demonstration purposes only.
          </p>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="relative z-10 py-8 text-center text-gray-500 text-sm border-t border-white/10">
        © {new Date().getFullYear()} ScrapX • Contact & Support
      </footer>
    </div>
  );
}
