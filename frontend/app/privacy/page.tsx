export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gray-50 px-6 py-12">
      <div className="mx-auto max-w-3xl rounded-2xl bg-white p-8 shadow">
        <h1 className="mb-4 text-3xl font-bold text-gray-900">Privacy Policy</h1>
        <p className="mb-4 text-gray-700">
          RevuIQ stores only the information needed to provide review analysis and account access for the configured deployment.
        </p>
        <div className="space-y-4 text-gray-700">
          <p><strong>Local authentication:</strong> Email signup data is stored in browser storage for the current frontend-only deployment.</p>
          <p><strong>Google authentication:</strong> Google login uses your selected Google profile name and email to create a RevuIQ session.</p>
          <p><strong>Review data:</strong> Reviews and analytics come from your configured backend/API integrations when available.</p>
          <p><strong>External APIs:</strong> Third-party review platform data is governed by each provider's privacy and API policies.</p>
        </div>
      </div>
    </div>
  );
}
