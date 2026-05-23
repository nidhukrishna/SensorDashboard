import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SensorDataset, ExtractedCycle
from .models import ExtractedCycle
from .waveform_analyzer import WaveformAnalyzer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class DatasetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        dataset_name = request.data.get('name', 'Untitled Dataset')
        
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        dataset = SensorDataset.objects.create(
            user=None,  # You can associate this with a user if you have authentication set up
            name=dataset_name,
            raw_file=file_obj
        )

        try:

            file_obj.seek(0)  # Ensure we're at the start of the file

            df = pd.read_csv(file_obj)
            
            time_col = df.columns[0]
            amp_col = df.columns[1]

            analyzer = WaveformAnalyzer(df[time_col], df[amp_col])
            results = analyzer.get_rise_fall_times()

            cycles_to_create = []
            for data in results:
                cycles_to_create.append(
                    ExtractedCycle(
                        dataset=dataset,
                        cycle_number=data['cycle_number'],
                        peak_time=data['peak_time'],
                        peak_amplitude=data['peak_amplitude'],
                        trough_time=data['trough_time'],
                        trough_amplitude=data['trough_amplitude'],
                        rise_time=data['rise_time'],
                        fall_time=data['fall_time']
                    )
                )
            
            ExtractedCycle.objects.bulk_create(cycles_to_create)

            dataset.is_processed = True
            dataset.save()

            return Response({
                "message": "Dataset processed successfully",
                "dataset_id": dataset.id,
                "cycles_extracted": len(cycles_to_create)
            }, status=201)

        except Exception as e:
            dataset.delete()
            return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def test_api(request):

    data = {
        "message": "Backend connected successfully"
    }

    return Response(data)

@api_view(['GET'])
def get_cycles(request):

    cycles = ExtractedCycle.objects.all()

    data = []

    for cycle in cycles:

        data.append({

            "cycle_number": cycle.cycle_number,
            "peak_time": cycle.peak_time,
            "peak_amplitude": cycle.peak_amplitude,
            "trough_time": cycle.trough_time,
            "trough_amplitude": cycle.trough_amplitude,
            "rise_time": cycle.rise_time,
            "fall_time": cycle.fall_time,

        })

    return Response(data)