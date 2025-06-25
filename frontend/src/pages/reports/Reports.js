import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiDownload, FiFilter, FiFileText, FiCalendar, FiClock, FiAlertTriangle } from 'react-icons/fi';
import { reportService, equipmentService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { format } from 'date-fns';

function Reports() {
  const { currentUser } = useAuth();
  const [reports, setReports] = useState([]);
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    type: '',
    equipment_id: '',
    date_from: '',
    date_to: '',
  });
  const [generatingReport, setGeneratingReport] = useState(false);
  const [selectedReportType, setSelectedReportType] = useState('health');
  const [selectedEquipment, setSelectedEquipment] = useState('');

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  // Carregar relatórios e equipamentos
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Em um ambiente real, descomentar estas linhas para buscar dados do backend
        // const reportsResponse = await reportService.getAllReports(filters);
        // setReports(reportsResponse.data);
        // const equipmentResponse = await equipmentService.getAllEquipment();
        // setEquipment(equipmentResponse.data);

        // Dados de exemplo para demonstração
        setReports([
          {
            id: '1',
            title: 'Análise de Saúde - Motor WEG W22',
            type: 'health',
            equipment_id: '1',
            equipment_name: 'Motor WEG W22',
            created_at: new Date('2024-05-15T10:30:00'),
            status: 'completed',
            summary: 'O equipamento apresenta risco médio de falha nos próximos 30 dias.',
            pdf_url: '#'
          },
          {
            id: '2',
            title: 'Histórico de Manutenção - Bomba Hidráulica KSB',
            type: 'maintenance',
            equipment_id: '2',
            equipment_name: 'Bomba Hidráulica KSB',
            created_at: new Date('2024-05-10T14:45:00'),
            status: 'completed',
            summary: 'Foram realizadas 3 manutenções preventivas nos últimos 90 dias.',
            pdf_url: '#'
          },
          {
            id: '3',
            title: 'Previsão de Falhas - Compressor Atlas Copco',
            type: 'prediction',
            equipment_id: '3',
            equipment_name: 'Compressor Atlas Copco',
            created_at: new Date('2024-05-05T09:15:00'),
            status: 'completed',
            summary: 'Probabilidade de 78% de falha no sistema de refrigeração nos próximos 60 dias.',
            pdf_url: '#'
          },
          {
            id: '4',
            title: 'Resumo Operacional - Trator Agrícola',
            type: 'summary',
            equipment_id: '4',
            equipment_name: 'Trator Agrícola',
            created_at: new Date('2024-04-28T16:20:00'),
            status: 'completed',
            summary: 'O equipamento operou por 450 horas no último mês com 2 alertas de alta temperatura.',
            pdf_url: '#'
          },
        ]);

        setEquipment([
          { id: '1', name: 'Motor WEG W22' },
          { id: '2', name: 'Bomba Hidráulica KSB' },
          { id: '3', name: 'Compressor Atlas Copco' },
          { id: '4', name: 'Trator Agrícola' },
          { id: '5', name: 'Esteira Transportadora' },
        ]);

        setLoading(false);
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  // Aplicar filtros
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  // Gerar novo relatório
  const handleGenerateReport = async () => {
    try {
      setGeneratingReport(true);
      
      // Em um ambiente real, descomentar estas linhas para gerar relatórios via backend
      // let response;
      // switch (selectedReportType) {
      //   case 'health':
      //     response = await reportService.generateHealthReport(selectedEquipment);
      //     break;
      //   case 'maintenance':
      //     response = await reportService.generateMaintenanceReport(selectedEquipment);
      //     break;
      //   case 'prediction':
      //     response = await reportService.generatePredictionReport(selectedEquipment);
      //     break;
      //   case 'summary':
      //     response = await reportService.generateSummaryReport();
      //     break;
      //   default:
      //     break;
      // }
      
      // Simulação de geração de relatório
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Adicionar relatório simulado à lista
      const newReport = {
        id: `temp-${Date.now()}`,
        title: `${getReportTypeName(selectedReportType)} - ${equipment.find(e => e.id === selectedEquipment)?.name || 'Todos os Equipamentos'}`,
        type: selectedReportType,
        equipment_id: selectedEquipment,
        equipment_name: equipment.find(e => e.id === selectedEquipment)?.name || 'Todos os Equipamentos',
        created_at: new Date(),
        status: 'completed',
        summary: 'Relatório gerado com sucesso.',
        pdf_url: '#'
      };
      
      setReports(prev => [newReport, ...prev]);
      setGeneratingReport(false);
      
      // Exibir mensagem de sucesso
      alert('Relatório gerado com sucesso!');
      
    } catch (error) {
      console.error('Erro ao gerar relatório:', error);
      setGeneratingReport(false);
      alert('Erro ao gerar relatório. Tente novamente.');
    }
  };

  // Baixar PDF do relatório
  const handleDownloadPdf = async (reportId) => {
    try {
      // Em um ambiente real, descomentar esta linha para baixar o PDF
      // const response = await reportService.generatePdfReport(reportId);
      // window.open(response.data.pdf_url, '_blank');
      
      // Simulação de download
      alert('Download do PDF iniciado!');
    } catch (error) {
      console.error('Erro ao baixar PDF:', error);
      alert('Erro ao baixar o PDF. Tente novamente.');
    }
  };

  // Obter nome amigável do tipo de relatório
  const getReportTypeName = (type) => {
    switch (type) {
      case 'health':
        return 'Análise de Saúde';
      case 'maintenance':
        return 'Histórico de Manutenção';
      case 'prediction':
        return 'Previsão de Falhas';
      case 'summary':
        return 'Resumo Operacional';
      default:
        return 'Relatório';
    }
  };

  // Obter ícone do tipo de relatório
  const getReportTypeIcon = (type) => {
    switch (type) {
      case 'health':
        return <FiAlertTriangle className="text-yellow-500" />;
      case 'maintenance':
        return <FiClock className="text-blue-500" />;
      case 'prediction':
        return <FiCalendar className="text-purple-500" />;
      case 'summary':
        return <FiFileText className="text-green-500" />;
      default:
        return <FiFileText className="text-gray-500" />;
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Relatórios Técnicos</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Filtros */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden lg:col-span-1">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Filtros</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="type" className="block text-sm font-medium text-gray-900 mb-1">Tipo de Relatório</label>
                <select
                  id="type"
                  name="type"
                  value={filters.type}
                  onChange={handleFilterChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Todos os tipos</option>
                  <option value="health">Análise de Saúde</option>
                  <option value="maintenance">Histórico de Manutenção</option>
                  <option value="prediction">Previsão de Falhas</option>
                  <option value="summary">Resumo Operacional</option>
                </select>
              </div>
              <div>
                <label htmlFor="equipment_id" className="block text-sm font-medium text-gray-900 mb-1">Equipamento</label>
                <select
                  id="equipment_id"
                  name="equipment_id"
                  value={filters.equipment_id}
                  onChange={handleFilterChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Todos os equipamentos</option>
                  {equipment.map(item => (
                    <option key={item.id} value={item.id}>{item.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="date_from" className="block text-sm font-medium text-gray-900 mb-1">Data Inicial</label>
                <input
                  type="date"
                  id="date_from"
                  name="date_from"
                  value={filters.date_from}
                  onChange={handleFilterChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label htmlFor="date_to" className="block text-sm font-medium text-gray-900 mb-1">Data Final</label>
                <input
                  type="date"
                  id="date_to"
                  name="date_to"
                  value={filters.date_to}
                  onChange={handleFilterChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Gerador de Relatórios */}
        <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden lg:col-span-2">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Gerar Novo Relatório</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="report_type" className="block text-sm font-medium text-gray-900 mb-1">Tipo de Relatório</label>
                <select
                  id="report_type"
                  value={selectedReportType}
                  onChange={(e) => setSelectedReportType(e.target.value)}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="health">Análise de Saúde</option>
                  <option value="maintenance">Histórico de Manutenção</option>
                  <option value="prediction">Previsão de Falhas</option>
                  <option value="summary">Resumo Operacional</option>
                </select>
              </div>
              <div>
                <label htmlFor="equipment_select" className="block text-sm font-medium text-gray-900 mb-1">Equipamento</label>
                <select
                  id="equipment_select"
                  value={selectedEquipment}
                  onChange={(e) => setSelectedEquipment(e.target.value)}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  disabled={selectedReportType === 'summary'}
                >
                  {selectedReportType === 'summary' ? (
                    <option value="">Todos os equipamentos</option>
                  ) : (
                    <>
                      <option value="">Selecione um equipamento</option>
                      {equipment.map(item => (
                        <option key={item.id} value={item.id}>{item.name}</option>
                      ))}
                    </>
                  )}
                </select>
              </div>
              <div className="pt-2">
                <button
                  onClick={handleGenerateReport}
                  disabled={generatingReport || (selectedReportType !== 'summary' && !selectedEquipment)}
                  className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all duration-200"
                >
                  {generatingReport ? 'Gerando...' : 'Gerar Relatório'}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Lista de Relatórios */}
      <motion.div variants={itemVariants} className="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Relatórios Disponíveis</h2>
          {loading ? (
            <p className="text-center py-4 text-gray-700">Carregando relatórios...</p>
          ) : reports.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Relatório</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Equipamento</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Data</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Resumo</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {reports.map((report) => (
                    <tr key={report.id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10 flex items-center justify-center bg-gray-100 rounded-full">
                            {getReportTypeIcon(report.type)}
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900">{report.title}</div>
                            <div className="text-sm text-gray-700">{getReportTypeName(report.type)}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{report.equipment_name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {format(report.created_at, 'dd/MM/yyyy')}
                        </div>
                        <div className="text-sm text-gray-700">
                          {format(report.created_at, 'HH:mm')}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900 max-w-xs truncate">{report.summary}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleDownloadPdf(report.id)}
                          className="text-primary-600 hover:text-primary-900 flex items-center transition-all duration-200 hover:scale-105"
                        >
                          <FiDownload className="mr-1" /> PDF
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-center py-4 text-gray-700">Nenhum relatório encontrado.</p>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}

export default Reports;