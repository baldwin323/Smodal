```typescript
// Import necessary Angular modules
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { DataService } from './services/data.service'; // Import data service to call API endpoints

// Define interface for AI response
interface AiResponse {
  response: string;
}

// Define interface for data
interface Data {
  input: string[];
}

// Define Component
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  // Declare variables
  currentPageIndex = 0;
  aiResponse: AiResponse | null = null; // Initialize aiResponse to null
  isLoading = false;
  data: Data = { input: [] };
  error: string | null = null;

  // Define a task map for dynamic function assignment
  taskMap = {
    'user-authentication': this.funcUserAuth,
    'dashboard': this.funcDashboard,
    // Add more tasks as necessary
  }

  // Inject services in the constructor
  constructor(private dataService: DataService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    this.runTask(this.pageIds[this.currentPageIndex]);
  }

  // Run the appropriate function based on the current task
  runTask(task) {
    if (task in this.taskMap) {
      this.taskMap[task]();
    } else {
      console.error(`No function mapped for task ${task}`);
    }
  }

  funcUserAuth() {
    // logic for user authentication
  }

  funcDashboard() {
    // logic for dashboard
  }

  // Fetch data through data service
  private fetchData(): Observable<AiResponse> {
    this.isLoading = true;
    
    return this.dataService.getAiPredict(this.data).pipe(
      catchError((error) => {
        this.isLoading = false;
        this.error = error.message;
        return throwError(error);
      })
    );
  }

  // Navigation functions seprated out the data fetch calls
  private navigate(indexModifier: number) {
    this.currentPageIndex += indexModifier;
    this.runTask(this.pageIds[this.currentPageIndex]);
  }
  
  handlePrevClick() {
    this.navigate(-1);
  }
  
  handleNextClick() {
    this.navigate(1);
  }
   
  // Document upload function
  onFileUpload(event: Event) {
    const file = (event.target as HTMLInputElement).files[0];
    const formData = new FormData();
    formData.append('file', file);

    this.dataService.uploadDocument(formData).subscribe(response => {
      if (response.success) {
        console.log('Document uploaded successfully');
      }
    });
  }
}
```
// The file is modified to include a task map for dynamic function assignment which improves flexibility and maintainability. The navigation functions now call the appropriate methods from the task map.
