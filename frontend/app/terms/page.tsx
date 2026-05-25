export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gray-50 px-6 py-12">
      <div className="mx-auto max-w-3xl rounded-2xl bg-white p-8 shadow">
        <h1 className="mb-4 text-3xl font-bold text-gray-900">Terms of Service</h1>
        <p className="mb-4 text-gray-700">
          RevuIQ provides review analytics, response drafting, and moderation tools for business review management.
        </p>
        <div className="space-y-4 text-gray-700">
          <p><strong>Account responsibility:</strong> You are responsible for the accuracy of account and business information you enter.</p>
          <p><strong>Generated responses:</strong> AI-generated responses should be reviewed before use. You remain responsible for published content.</p>
          <p><strong>Third-party platforms:</strong> Google, Yelp, Meta, and other platform integrations require valid API credentials and compliance with each provider's terms.</p>
          <p><strong>Data:</strong> Local demo data stored in your browser remains on your device. Connected backend data is handled by your configured backend service.</p>
        </div>
      </div>
    </div>
  );
}
