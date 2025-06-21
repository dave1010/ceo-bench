import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Github, FileText, Trophy, BarChart3, Users, Target, ArrowRight } from "lucide-react"
import Link from "next/link"
import Leaderboard from "@/components/Leaderboard"
import ModelsBarChart from "@/components/ModelsBarChart"
import { loadLeaderboard } from '@/lib/leaderboard'

export default async function Component() {
  const rows = await loadLeaderboard()
  const scenarioCount = rows.reduce((m, r) => Math.max(m, Number(r.n)), 0)
  const llmCount = rows.length
  const topicKeys = rows[0]
    ? Object.keys(rows[0]).filter(k => !['model', 'model_name', 'overall', 'n'].includes(k))
    : []
  const compCount = topicKeys.length
  const topScore = rows.reduce((m, r) => Math.max(m, Number(r.overall)), 0)

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Header */}
      <header className="border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between px-4 md:px-6">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-slate-900 text-white rounded-lg font-bold text-lg">
              CEO
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">CEO Bench</h1>
              <p className="text-xs text-slate-600">LLM Executive Evaluation</p>
            </div>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="#leaderboard" className="text-sm font-medium text-slate-700 hover:text-slate-900">
              Leaderboard
            </Link>
            <Link href="#methodology" className="text-sm font-medium text-slate-700 hover:text-slate-900">
              Methodology
            </Link>
            <Link href="#about" className="text-sm font-medium text-slate-700 hover:text-slate-900">
              About
            </Link>
          </nav>
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm" asChild>
              <Link href="https://github.com/dave1010/ceo-bench" className="flex items-center space-x-2">
                <Github className="w-4 h-4" />
                <span className="hidden sm:inline">GitHub</span>
              </Link>
            </Button>
            <Button size="sm" asChild>
              <Link href="#" className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span className="hidden sm:inline">Paper</span>
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="py-20 md:py-32 bg-gradient-to-b from-slate-50 to-white">
          <div className="container px-4 md:px-6">
            <div className="max-w-4xl mx-auto text-center space-y-8">
              <div className="space-y-4">
                <Badge variant="secondary" className="text-sm font-medium">
                  Research Benchmark
                </Badge>
                <h1 className="text-4xl md:text-6xl font-bold text-slate-900 leading-tight">
                  Can AI Replace the
                  <span className="text-slate-700"> C-Suite?</span>
                </h1>
                <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
                  CEO Bench is an open benchmark measuring how well large language models tackle
                  executive decision making, strategic planning and leadership challenges.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button size="lg" asChild className="bg-slate-900 hover:bg-slate-800">
                  <Link href="#leaderboard" className="flex items-center space-x-2">
                    <Trophy className="w-5 h-5" />
                    <span>View Leaderboard</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </Button>
                <Button variant="outline" size="lg" asChild>
                  <Link href="https://github.com/dave1010/ceo-bench#readme" className="flex items-center space-x-2">
                    <FileText className="w-5 h-5" />
                    <span>Read the Docs</span>
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 bg-white border-y">
          <div className="container px-4 md:px-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-slate-900">{scenarioCount}</div>
                <div className="text-sm text-slate-600 mt-1">Executive Scenarios</div>
              </div>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-slate-900">{llmCount}</div>
                <div className="text-sm text-slate-600 mt-1">Leading LLMs Tested</div>
              </div>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-slate-900">{compCount}</div>
                <div className="text-sm text-slate-600 mt-1">Core Competencies</div>
              </div>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-slate-900">{topScore.toFixed(1)}</div>
                <div className="text-sm text-slate-600 mt-1">Top Model Score</div>
              </div>
            </div>
          </div>
        </section>

        {/* Leaderboard Section */}
        <section id="leaderboard" className="py-20 bg-slate-50">
          <div className="container px-4 md:px-6">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Current Leaderboard</h2>
                <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                  Rankings based on comprehensive evaluation across strategic thinking, operational excellence,
                  leadership capabilities, and financial acumen.
                </p>
              </div>

              <div className="mb-8">
                <ModelsBarChart rows={rows} />
              </div>

              <Leaderboard />
            </div>
          </div>
        </section>

        {/* Methodology Section */}
        <section id="methodology" className="py-20 bg-white">
          <div className="container px-4 md:px-6">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Evaluation Methodology</h2>
                <p className="text-lg text-slate-600">
                  Our benchmark evaluates LLMs across four critical executive competencies
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Target className="w-5 h-5 text-slate-700" />
                      <span>Strategic Thinking</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 mb-4">
                      Long-term planning, market analysis, competitive positioning, and vision setting capabilities.
                    </p>
                    <ul className="text-sm text-slate-600 space-y-1">
                      <li>• Market entry strategies</li>
                      <li>• Competitive analysis</li>
                      <li>• Long-term planning</li>
                      <li>• Vision articulation</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="w-5 h-5 text-slate-700" />
                      <span>Operational Excellence</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 mb-4">
                      Process optimization, resource allocation, performance management, and operational efficiency.
                    </p>
                    <ul className="text-sm text-slate-600 space-y-1">
                      <li>• Resource optimization</li>
                      <li>• Process improvement</li>
                      <li>• Performance metrics</li>
                      <li>• Efficiency analysis</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Users className="w-5 h-5 text-slate-700" />
                      <span>Leadership & Communication</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 mb-4">
                      Team management, stakeholder communication, crisis management, and organizational culture.
                    </p>
                    <ul className="text-sm text-slate-600 space-y-1">
                      <li>• Team motivation</li>
                      <li>• Stakeholder management</li>
                      <li>• Crisis communication</li>
                      <li>• Culture building</li>
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <FileText className="w-5 h-5 text-slate-700" />
                      <span>Financial Acumen</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-600 mb-4">
                      Financial analysis, budgeting, investment decisions, and risk assessment capabilities.
                    </p>
                    <ul className="text-sm text-slate-600 space-y-1">
                      <li>• Financial modeling</li>
                      <li>• Investment analysis</li>
                      <li>• Risk assessment</li>
                      <li>• Budget planning</li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section id="about" className="py-20 bg-slate-50">
          <div className="container px-4 md:px-6">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">About CEO Bench</h2>
              <p className="text-lg text-slate-600 mb-8 leading-relaxed">
                CEO Bench is an open research benchmark for evaluating large language models on executive leadership tasks.
                It generates realistic management questions, collects model answers and scores them automatically to build the leaderboard below.
              </p>
              <p className="text-lg text-slate-600 mb-8 leading-relaxed">
                The Python scripts powering this site are included in the repository so you can run your own evaluations
                or extend the question set.
              </p>
              <p className="text-lg text-slate-600 mb-8 leading-relaxed">
                All data and code are released under the MIT License and contributions are welcome.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button variant="outline" size="lg" asChild>
                  <Link href="https://github.com/dave1010/ceo-bench" className="flex items-center space-x-2">
                    <Github className="w-5 h-5" />
                    <span>Explore on GitHub</span>
                  </Link>
                </Button>
                <Button variant="outline" size="lg" asChild>
                  <Link href="https://github.com/dave1010/ceo-bench#readme" className="flex items-center space-x-2">
                    <FileText className="w-5 h-5" />
                    <span>Read the Docs</span>
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white py-12">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="flex items-center justify-center w-8 h-8 bg-slate-900 text-white rounded font-bold text-sm">
                CEO
              </div>
              <span className="font-semibold text-slate-900">CEO Bench</span>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t text-center text-sm text-slate-500">
            <p>
              &copy; 2025 <a href="https://dave.engineer" className="underline hover:text-slate-700" target="_blank" rel="noopener noreferrer">Dave Hulbert</a>. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
